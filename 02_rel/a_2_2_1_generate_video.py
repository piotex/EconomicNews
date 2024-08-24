import os
import time
import random
import cv2 as cv
from PIL import Image
from news_model import *
from mutagen.mp3 import MP3
from moviepy.editor import *

frames = 25
width = 1080
height = 1920


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


def get_subtitles_list(file_path: str):
    res = []
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.readlines()
        for i in range(len(text)):
            if "-->" in text[i]:
                tmp = text[i].split("-->")
                start_ms = convert_to_ms(tmp[0])
                end_ms = convert_to_ms(tmp[1])
                tmp_txt = ""
                for j in range(1, len(text) - i):
                    if "-->" in text[i + j] or i + j == len(text) - 1:
                        tmp_txt = tmp_txt.replace("\n", "").replace("-", "")
                        res.append([start_ms, end_ms, update_text(tmp_txt)])
                        break
                    tmp_txt += text[i + j]
        return res


def get_audio_files(audios_path: str):
    files_in_folder = os.listdir(audios_path)
    files_in_folder = [a.split(".")[0] for a in files_in_folder if ".mp3" in a]

    audio_files = []
    for file in files_in_folder:
        file_name = audios_path + "/" + file + ".mp3"
        file_name = os.path.abspath(file_name)
        start = 0
        end = get_audio_length(file_name)
        audio_files.append([start, end, file_name])

    for i in range(1, len(audio_files), 1):
        start = audio_files[i][0] + audio_files[i - 1][1]
        end = audio_files[i][1] + audio_files[i - 1][1]
        audio_files[i] = [start, end, audio_files[i][2]]
    return audio_files


def get_subtitles(audios_path: str) -> list[list[str]]:  # start | end | text
    files_in_folder = os.listdir(audios_path)
    files_in_folder = [a.split(".")[0] for a in files_in_folder if ".mp3" in a]
    subtitles_list = []
    for file in files_in_folder:
        new_subtitles = get_subtitles_list(audios_path + "/" + file + ".vvt")
        file_name = audios_path + "/" + file + ".mp3"
        end = get_audio_length(file_name)
        new_subtitles[-1][1] = end

        subtitles_list += [new_subtitles[0]]
        for i in range(1, len(new_subtitles)):
            new_start = new_subtitles[i][0] - new_subtitles[i - 1][1]
            new_end = new_subtitles[i][1] - new_subtitles[i - 1][1]
            subtitles_list.append([new_start, new_end, new_subtitles[i][2]])

    res = [subtitles_list[0]]
    for i in range(1, len(subtitles_list), 1):
        new_start = subtitles_list[i][0] + res[i - 1][1]
        new_end = subtitles_list[i][1] + res[i - 1][1]
        res.append([new_start, new_end, subtitles_list[i][2]])
    return res


def get_video_end_time(subtitles) -> int:
    return subtitles[-1][1]


def get_video_length(filename):
    cap = cv.VideoCapture(filename)
    fps = cap.get(cv.CAP_PROP_FPS)
    frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    duration_ms = int(frame_count / fps * 1000)
    cap.release()
    return duration_ms


def get_audio_length(filename):
    return int(MP3(filename).info.length * 1000)


def generate_background_clips(audios_path: str):
    subtitles = get_subtitles(audios_path)
    video_length_ms = get_video_end_time(subtitles)

    folder = "data/videos/background_videos"
    # folder = "02_rel/data/videos/background_videos"
    file_name = folder + "/" + os.listdir(folder)[random.randrange(len(os.listdir(folder)))]

    random_start_time_ms = random.randint(video_length_ms + 1, get_video_length(file_name) - 10)
    background_clip = VideoFileClip(file_name).subclip((random_start_time_ms / 1000), (random_start_time_ms / 1000) + (video_length_ms / 1000)+1)
    background_clip = background_clip.resize((width, height))

    return [background_clip]


def generate_subtitles_clip(audios_path: str):
    font_size = 65
    text_clips = []
    subtitles = get_subtitles(audios_path)
    for subtitle in subtitles:
        start_ms = int(subtitle[0])
        end_ms = int(subtitle[1])
        text = subtitle[2]

        pos = (120, 800)
        pos = "center"
        txt_clip = TextClip(text, fontsize=font_size, color='white', stroke_color='black', stroke_width=12).set_pos(
            pos).set_start(start_ms / 1000).set_duration((end_ms - start_ms) / 1000)
        text_clips.append(txt_clip)
        txt_clip = TextClip(text, fontsize=font_size, color='white').set_pos(pos).set_duration(
            (end_ms - start_ms) / 1000).set_start(start_ms / 1000)
        text_clips.append(txt_clip)
    return text_clips


def generate_bird_clip(audios_path: str):
    folder = "data/images/animated_bird"
    # folder = "02_rel/data/images/animated_bird"
    bird_clips = []
    bird_width = 400
    bird_height = 400
    old_start_ms = random.randint(1000, 2000)
    old_file_name = ""
    subtitles = get_subtitles(audios_path)
    video_length_ms = get_video_end_time(subtitles)
    while old_start_ms < video_length_ms:
        rand_pos_x = random.randint(0, width - bird_width)
        rand_pos_y = random.randint(1200, height - bird_height)
        pos = (rand_pos_x, rand_pos_y)

        rand_duration = random.randint(2000, 4000)
        if old_start_ms + rand_duration > video_length_ms:
            rand_duration = video_length_ms - old_start_ms

        file_name = folder + "/" + os.listdir(folder)[random.randrange(len(os.listdir(folder)))]
        while file_name == old_file_name:
            file_name = folder + "/" + os.listdir(folder)[random.randrange(len(os.listdir(folder)))]

        img = ImageClip(file_name).resize((bird_width, bird_height)).set_pos(pos).set_duration(
            rand_duration / 1000).set_start(old_start_ms / 1000)
        bird_clips.append(img)
        old_start_ms += rand_duration
    return bird_clips


def generate_screenshot_clip(audios_path: str, screenshots_path: str):
    subtitles = get_subtitles(audios_path)

    video_length_ms = get_video_end_time(subtitles)

    files_in_folder = os.listdir(screenshots_path)
    files_in_folder = [screenshots_path + "/" + a for a in files_in_folder if "." in a]
    screenshots_clips = []
    for i, file in enumerate(files_in_folder):
        screenshot_length = int(video_length_ms / len(files_in_folder))
        img_wh = Image.open(file).size
        resize = (width - 100, img_wh[1] * ((width - 100) / img_wh[0]))
        pos = (50, 300 + 100 * random.uniform(0.8, 1.2))
        img = ImageClip(file).resize(resize).set_pos(pos).set_start(i * screenshot_length / 1000).set_duration(screenshot_length / 1000)
        screenshots_clips.append(img)
    return screenshots_clips


def generate_audio_clip(audios_path: str):
    audio_files_clips = []
    audio_files = get_audio_files(audios_path)
    for audio_file in audio_files:
        audio_clip = AudioFileClip(audio_file[2]).set_start(audio_file[0] / 1000)#.set_duration((audio_file[1] / 1000) - (audio_file[0] / 1000))
        audio_files_clips.append(audio_clip)
    new_audio_clip = CompositeAudioClip(audio_files_clips)
    return new_audio_clip


def main():
    model_list = load_obj_list()
    for i, model in enumerate(model_list):
        audios_path = f"data/audios/{i}"
        screenshots_path = f"data/images/screenshots/{i}"
        # folder = "02_rel/data/images/screenshots"

        background_clip = generate_background_clips(audios_path)
        subtitles_clip = generate_subtitles_clip(audios_path)
        bird_clip = generate_bird_clip(audios_path)
        screenshot_clip = generate_screenshot_clip(audios_path, screenshots_path)
        audio_clip = generate_audio_clip(audios_path)

        all_clips = background_clip + screenshot_clip + bird_clip + subtitles_clip
        video = CompositeVideoClip(all_clips, size=(width, height))
        video.audio = audio_clip

        video_path = f'data/videos/for_publication/{i}/result.mp4'
        # video.write_videofile('02_rel/data/result.mp4')
        video.write_videofile(video_path)
        model.video_path = video_path
        save_obj_list(model_list)


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
