from datetime import timedelta
from news_model import *


def limit_1(news: NewsModel):
    return news.creation_date < datetime.now() - timedelta(days=1)


def get_unique(news_list: list[NewsModel]):
    unique_news = []
    dict_m = {}
    for elem in news_list:
        if elem.url not in dict_m:
            unique_news.append(elem)
            dict_m[elem.url] = 0
    return unique_news


def sort_by_comments_count(news_list: list[NewsModel]):
    return sorted(news_list, key=lambda news: news.comments_count, reverse=True)


def main():
    limit_news_to_proceed = 1
    result = []
    obj_list = load_obj_list()
    obj_list = get_unique(obj_list)
    obj_list = sort_by_comments_count(obj_list)
    count = 1
    for obj_m in obj_list:
        if count > limit_news_to_proceed:
            break

        if limit_1(obj_m):
            continue

        result.append(obj_m)
        count += 1
    save_obj_list(result)


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
