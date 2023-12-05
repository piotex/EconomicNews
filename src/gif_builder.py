import json
import sys
import dataclasses
import numpy as np
from models.model_news import NewsModel
from PIL import Image, ImageDraw, ImageFont
from general_utils import get_idx_to_process

video_fps = 30
max_str_len = 25
font_size = 70
thickness = 3
my_font = "../data_files/arial.ttf"


def draw_text_line(draw, x_offset, y_offset, text):
    draw.text((x_offset - thickness, y_offset - thickness), text, fill="black",
              font=ImageFont.truetype(my_font, font_size), anchor="mm", align="center")
    draw.text((x_offset + thickness, y_offset - thickness), text, fill="black",
              font=ImageFont.truetype(my_font, font_size), anchor="mm", align="center")
    draw.text((x_offset - thickness, y_offset + thickness), text, fill="black",
              font=ImageFont.truetype(my_font, font_size), anchor="mm", align="center")
    draw.text((x_offset + thickness, y_offset + thickness), text, fill="black",
              font=ImageFont.truetype(my_font, font_size), anchor="mm", align="center")

    draw.text((x_offset, y_offset), text, fill="white", font=ImageFont.truetype(my_font, font_size), anchor="mm",
              align="center")


def draw_text(resized_image_in, text: str):
    draw = ImageDraw.Draw(resized_image_in)
    y_offset = resized_image_in.height // 2 + 450
    x_offset = resized_image_in.width // 2

    text_tab = text.split("\n")
    i = 0
    for data in text_tab:
        draw_text_line(draw, x_offset, y_offset + (i * font_size), data)
        i += 1


def get_klatka_start(data: str):
    data_start = data.split(" --> ")[0]
    data_start_m = int(data_start.split(":")[1])
    data_start_s = int(data_start.split(":")[2].split(".")[0])
    data_start_ms = int(data_start.split(":")[2].split(".")[1])
    time_start_ms = int((((data_start_m * 60) + data_start_s) * 1000) + data_start_ms)
    klatka_start = int(time_start_ms / 1000 * video_fps)
    return klatka_start


def get_klatka_end(data: str):
    data_end = data.split(" --> ")[1]
    data_end_m = int(data_end.split(":")[1])
    data_end_s = int(data_end.split(":")[2].split(".")[0])
    data_end_ms = int(data_end.split(":")[2].split(".")[1])
    time_end_ms = int((((data_end_m * 60) + data_end_s) * 1000) + data_end_ms)
    klatka_end = int(time_end_ms / 1000 * video_fps)
    return klatka_end


def get_start_stop_text_tab(vvt_path, raw_text):
    time_tab = []
    data_tab = []
    raw_data = []
    with open(vvt_path, 'r') as plik:
        raw_data = plik.readlines()

    for i in range(len(raw_data)):
        raw_data[i] = raw_data[i].replace("-\n", "")
        raw_data[i] = raw_data[i].replace("\n", "")

    for i in range(len(raw_data)):
        if " --> " in raw_data[i]:
            time_tab.append(raw_data[i])
            i += 1
            tmp_str = ""
            while raw_data[i] != "":
                tmp_str += raw_data[i]
                i += 1
            data_tab.append(tmp_str)

    res = []  # [start | stop | text]
    end_tmppp = get_klatka_end(time_tab[-1])
    data_tab = raw_text.split(". ")
    chunk_tmppp = end_tmppp // len(data_tab)
    for i in range(len(data_tab)):
        start = chunk_tmppp * i + 0
        stop = chunk_tmppp * i + chunk_tmppp - 1

        row_text_tab = []
        row_text_split = data_tab[i].split()
        if len(row_text_split) == 0:
            continue

        tmp_str = ""
        for j in range(len(row_text_split) - 1):
            tmp_str += row_text_split[j] + " "
            if len(row_text_split[j + 1] + tmp_str) > max_str_len:
                row_text_tab.append(tmp_str[:-1])
                tmp_str = ""

        last_word = row_text_split[-1]
        if len(last_word + tmp_str) > max_str_len:
            row_text_tab.append(tmp_str)
            row_text_tab.append(last_word)
        else:
            row_text_tab.append(tmp_str + " " + last_word)
        tmp_str_2 = '\n'.join(row_text_tab)
        res.append([start, stop, tmp_str_2])
    return res


def update_time_quicker_subtitles(start_stop_text_tab):
    d_klatka = 15
    start_stop_text_tab[0][1] -= d_klatka
    for i in range(1, len(start_stop_text_tab)):
        start_stop_text_tab[i][0] -= d_klatka
        start_stop_text_tab[i][1] -= d_klatka
    return start_stop_text_tab


def generate_gif_from_img_vvt(input_image_path, vvt_path, out_path, raw_text):
    start_stop_text_tab = get_start_stop_text_tab(vvt_path, raw_text)
    input_image = Image.open(input_image_path)
    width, height = input_image.size

    ilosc_klatek = start_stop_text_tab[-1][1]
    total_time_s = ilosc_klatek / video_fps
    zoom_levels = np.linspace(1.5, 1, ilosc_klatek)

    zoomed_images = []
    # start_stop_text_tab = update_time_quicker_subtitles(start_stop_text_tab)
    for i in range(0, ilosc_klatek, 1):

        zoom_level = zoom_levels[i]
        new_width = int(width * zoom_level)
        new_height = int(height * zoom_level)

        x_offset = int((new_width - width) / 2)
        y_offset = int((new_height - height) / 2)

        resized_image = input_image.resize((new_width, new_height), Image.LANCZOS)
        resized_image = resized_image.crop((x_offset, y_offset, width + x_offset, height + y_offset))

        for start, stop, text in start_stop_text_tab:
            if start <= i <= stop:
                draw_text(resized_image, text)
                break

        zoomed_images.append(resized_image)

    zoomed_images[0].save(out_path, save_all=True, append_images=zoomed_images, optimize=False, duration=total_time_s)
    del zoomed_images
    zoomed_images = None
    # , loop=0


def gif_builder(idx_to_process):
    func_name = "gif_builder"
    print(f"{func_name}: {idx_to_process}")

    path_news_list = "../data_files/important_files/news_list.json"
    with open(path_news_list, "r") as json_file:
        data_from_json = json.load(json_file)
    my_class_objects = [NewsModel(**item) for item in data_from_json]

    idx = 0
    for elem in my_class_objects:
        if idx == idx_to_process:
            elem.video_quick_info_gif_path = f"../data_files/gifs/{elem.id}.gif_builder.gif"
            generate_gif_from_img_vvt(elem.screen_path, elem.audio_quick_info_vvt_path, elem.video_quick_info_gif_path,
                                      elem.quick_info)
            break
        idx += 1

    news_dict_list = [dataclasses.asdict(news) for news in my_class_objects]
    with open(path_news_list, "w") as json_file:
        json.dump(news_dict_list, json_file, indent=4)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        idx_to_process_arg = get_idx_to_process()
        gif_builder(idx_to_process_arg)
    else:
        for i in range(5):
            gif_builder(i)
