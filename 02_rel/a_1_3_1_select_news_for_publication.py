from news_model import *
import time

obj_list_path = "data/obj_list.json"


def sort_obj_list_by_comments(news_model_list: list[NewsModel]) -> list[NewsModel]:
    return sorted(news_model_list, key=lambda model: model.comments_count, reverse=True)


def find_not_processed_news(news_model_list: list[NewsModel]) -> NewsModel:
    with open("data/urls/processed_news.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        lines = [l.strip().replace('\n', '') for l in lines]
    for news in news_model_list:
        if news not in lines:
            return news
    raise Exception("=== All news already processed ===")


def filter_news_by_comments(news_model_list: list[NewsModel]) -> list[NewsModel]:
    min_comments_count = 3
    news_model_list = sort_obj_list_by_comments(news_model_list)
    if news_model_list[0].comments_count < min_comments_count:
        raise Exception("=== Boring News ===")
    return news_model_list


def main():
    main_list_of_obj = load_obj_list()
    main_list_of_obj = filter_news_by_comments(main_list_of_obj)
    news = find_not_processed_news(main_list_of_obj)
    save_obj(news)

    main_list_of_obj = sort_obj_list_by_comments(main_list_of_obj)
    save_obj_list(main_list_of_obj)


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
