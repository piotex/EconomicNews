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
    # print(f"init_folders")
    # init_folders()
    # print(f"get_raw_info")
    # get_raw_info()
    # print(f"filter_by_creation_time")
    # filter_by_creation_time()
    # print(f"get_comments_count")
    # get_comments_count()
    # print(f"sort_by_comments_count")
    # sort_by_comments_count()
    # print(f"text_to_speech")
    # text_to_speech()
    print(f"gif_builder")
    gif_builder()
    print(f"video_builder")
    video_builder()
    print(f"video_merge")
    video_merge()
    print(f"yt_publisher")
    yt_publisher()


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"")
    print(f"#####################################")
    print(f"Total time: {end_time - start_time} s")
    print(f"#####################################")
