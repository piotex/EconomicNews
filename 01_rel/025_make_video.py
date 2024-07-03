import random
from moviepy.editor import *
from news_model import *

frames = 25


@dataclass
class NewsModel:
    idx: str = ""
    url: str = ""
    comments_count: int = -1
    article_text: str = ""

    creation_date: datetime = datetime.now()
    actualization_date: datetime = datetime.now()

    img_dir_path: str = ""
    vvt_path: str = ""
    mp3_path: str = ""


def convert_to_ms(text: str):
    text = text.strip()
    numbs = text.split(":")
    res = int(numbs[0]) * 1000 * 60 + int(numbs[1]) * 1000 * 60
    numbs = numbs[2].split(".")
    res += int(numbs[0]) * 1000 + int(numbs[1])
    return res


def update_text(text: str):
    max_len = 30
    words = text.split()
    res = ""
    line = ""
    for word in words:
        if len(line + word + " ") < max_len:
            line += word + " "
        else:
            res += line + "\n"
            line = word + " "
    res += line
    return res


def get_subtitles_list(model: NewsModel):
    my_obj = load_obj_list()[0]
    res = []
    with open(my_obj.vvt_path, "r", encoding="utf-8") as f:
        text = f.readlines()
        for i in range(len(text)):
            if text[i][0].isdigit():
                tmp = text[i].split("-->")
                start_ms = convert_to_ms(tmp[0])
                end_ms = convert_to_ms(tmp[1])
                tmp_txt = ""
                for j in range(1, len(text) - i):
                    if text[i + j][0].isdigit() or i + j == len(text) - 1:
                        tmp_txt = tmp_txt.replace("\n", "").replace("-", "")
                        res.append([start_ms, end_ms, update_text(tmp_txt)])
                        break
                    tmp_txt += text[i + j]
        return res


def main():
    width = 1080
    height = 1920

    model = load_obj_list()[0]
    subtitles = get_subtitles_list(model)

    folder = "data/background_videos"
    file_name = folder + "/" + os.listdir(folder)[random.randrange(len(os.listdir(folder)))]
    background_clip = VideoFileClip(file_name).subclip(0, subtitles[-1][1] / 1000)
    background_clip = background_clip.resize((width, height))

    text_clips = []
    for subtitle in subtitles:
        start_ms = subtitle[0]
        end_ms = subtitle[1]
        text = subtitle[2]

        txt_clip = TextClip(text, fontsize=75, color='white', stroke_color='black', stroke_width=12).set_pos(
            'center').set_duration((end_ms - start_ms) / 1000).set_start(start_ms / 1000)
        text_clips.append(txt_clip)
        txt_clip = TextClip(text, fontsize=75, color='white').set_pos('center').set_duration(
            (end_ms - start_ms) / 1000).set_start(start_ms / 1000)
        text_clips.append(txt_clip)

    max_time_ms = subtitles[-1][1]
    folder = "data/animated_bird"
    bird_clips = []
    bird_width = 400
    bird_heigth = 400
    old_start_ms = random.randint(1000, 2000)
    old_file_name = ""
    while old_start_ms < max_time_ms:
        rand_pos_x = random.randint(0, width - bird_width)
        rand_pos_y = random.randint(0, 500)
        rand_duration = random.randint(2000, 4000)
        if old_start_ms + rand_duration > max_time_ms:
            rand_duration = max_time_ms - old_start_ms

        file_name = folder + "/" + os.listdir(folder)[random.randrange(len(os.listdir(folder)))]
        while file_name == old_file_name:
            file_name = folder + "/" + os.listdir(folder)[random.randrange(len(os.listdir(folder)))]

        img = ImageClip(file_name).resize((bird_width, bird_heigth)).set_pos((rand_pos_x, rand_pos_y)).set_duration(
            rand_duration / 1000).set_start(old_start_ms / 1000)
        bird_clips.append(img)
        old_start_ms += rand_duration

    audioclip = AudioFileClip(model.mp3_path)
    new_audioclip = CompositeAudioClip([audioclip])

    all_clips = [background_clip] + bird_clips + text_clips
    video = CompositeVideoClip(all_clips, size=(width, height))
    video.audio = new_audioclip
    video.write_videofile('data/result.mp4')
    a = 0


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    total_s = end_time - start_time
    total_m = int(total_s / 60)
    total_s = int(total_s - total_m * 60)
    print(f"")
    print(f"#####################################")
    print(f"Total time: {total_m}m {total_s}s")
    print(f"#####################################")
