import dataclasses
import json
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.editor import VideoFileClip, AudioFileClip
from src.models.model_news import NewsModel


def video_merge():
    video_fps = 30
    path_in_data = "../data_files/important_files/7_video_builder.json"

    with open(path_in_data, "r") as json_file:
        data_from_json = json.load(json_file)
    my_class_objects = [NewsModel(**item) for item in data_from_json]

    file_paths = []
    for elem in my_class_objects:
        file_paths.append(elem.video_quick_info_mp4_path)

    mp4_path = f"../data_files/movies/final.mp4"
    video_clips = [VideoFileClip(path) for path in file_paths]
    final_clip = concatenate_videoclips(video_clips)
    final_clip.write_videofile(mp4_path, codec="libx264", fps=video_fps)


if __name__ == "__main__":
    video_merge()
