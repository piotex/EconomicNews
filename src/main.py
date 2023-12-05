import time
from filter_by_creation_time import filter_by_creation_time
from get_comments_count import get_comments_count
from get_raw_info import get_raw_info
from gif_builder import gif_builder
from init_folders import init_folders
from sort_by_comments_count import sort_by_comments_count
from text_to_speech import text_to_speech
from video_builder import video_builder
from video_merge import video_merge
from yt_publisher import yt_publisher


def main():
    print(f"")
    init_folders()
    get_raw_info()
    filter_by_creation_time()
    get_comments_count()
    sort_by_comments_count()

    for i in range(5):
        text_to_speech(i)
        gif_builder(i)

    for i in range(5):
        video_builder(i)

    video_merge()
    yt_publisher()


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"")
    print(f"#####################################")
    print(f"Total time: {end_time - start_time} s")
    print(f"#####################################")
