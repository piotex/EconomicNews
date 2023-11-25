from src.filter_by_creation_time import filter_by_creation_time
from src.get_comments_count import get_comments_count
from src.get_raw_info import get_raw_info
from src.gif_builder import gif_builder
from src.sort_by_comments_count import sort_by_comments_count
from src.text_to_speech import text_to_speech
from src.video_builder import video_builder
from src.video_merge import video_merge

print("hello worlds")

init_folders()
get_raw_info()
filter_by_creation_time()
get_comments_count()
sort_by_comments_count()
text_to_speech()
gif_builder()
video_builder()
video_merge()

# get_raw_info
# filter_by_creation_time
# get_comments_count
# sort_by_comments_count
#
# text_to_speech
# gif_builder
# video_builder


