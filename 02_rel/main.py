import time
import a_0_1_1_init_files_and_dirs as a_0_1_1_init_files_and_dirs
import a_1_1_1_get_news_from_main_pages as a_1_1_1_get_news_from_main_pages
import a_1_2_1_get_news_details as a_1_2_1_get_news_details
import a_1_3_1_select_news_for_publication as a_1_3_1_select_news_for_publication
import a_1_4_1_get_news_screenshots as a_1_4_1_get_news_screenshots
import a_1_5_1_parse_article_with_ai as a_1_5_1_parse_article_with_ai
import a_2_1_1_generate_voice_over_with_ai as a_2_1_1_generate_voice_over_with_ai
import a_2_2_1_generate_video as a_2_2_1_generate_video
import a_3_1_1_publish_video_on_youtube as a_3_1_1_publish_video_on_youtube

def get_time(start_time):
    end_time = time.time()
    total_s = end_time - start_time
    total_m = int(total_s / 60)
    total_s = int(total_s - total_m * 60)
    return f"{total_m}m {total_s}s"

if __name__ == "__main__":
    start_time = time.time()
    # a_0_1_1_init_files_and_dirs.main()
    # print(f"a_0_1_1_init_files_and_dirs time: {get_time(start_time)}")
    # a_1_1_1_get_news_from_main_pages.main()
    # print(f"a_1_1_1_get_news_from_main_pages time: {get_time(start_time)}")
    # a_1_2_1_get_news_details.main()
    # print(f"a_1_2_1_get_news_details time: {get_time(start_time)}")
    # a_1_3_1_select_news_for_publication.main()
    # print(f"a_1_3_1_select_news_for_publication time: {get_time(start_time)}")
    # a_1_4_1_get_news_screenshots.main()
    # print(f"a_1_4_1_get_news_screenshots time: {get_time(start_time)}")
    # a_1_5_1_parse_article_with_ai.main()
    # print(f"a_1_5_1_parse_article_with_ai time: {get_time(start_time)}")
    # a_2_1_1_generate_voice_over_with_ai.main()
    # print(f"a_2_1_1_generate_voice_over_with_ai time: {get_time(start_time)}")
    a_2_2_1_generate_video.main()
    print(f"a_2_2_1_generate_video time: {get_time(start_time)}")
    a_3_1_1_publish_video_on_youtube.main()
    print(f"a_3_1_1_publish_video_on_youtube time: {get_time(start_time)}")
    print(f"")
    print(f"#####################################")
    print(f"Total time: {int(time.time() - start_time / 60)}m {int(time.time() - start_time - int(time.time() - start_time / 60) * 60)}s")
    print(f"#####################################")