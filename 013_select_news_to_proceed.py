import json
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

obj_list_path = "data/obj_list.json"


@dataclass
class NewsModel:
    url: str = ""
    creation_date: datetime = datetime.now()
    actualization_date: datetime = datetime.now()
    comments_count: int = -1
    article_text: str = ""
    article_img: str = ""


def load_obj_list() -> list[NewsModel]:
    with open(obj_list_path, "r") as f:
        list_of_users = json.load(f)
        list_of_users = [NewsModel(**item) for item in list_of_users]
        for a in list_of_users:
            a.creation_date = datetime.strptime(str(a.creation_date), "%Y-%m-%d %H:%M:%S")
            a.actualization_date = datetime.strptime(str(a.actualization_date), "%Y-%m-%d %H:%M:%S")
    return list_of_users


def limit_1(news: NewsModel):
    return news.creation_date < datetime.now() - timedelta(days=1)


def save_obj_list(news_list: list[NewsModel]):
    with open(obj_list_path, "w", encoding="utf-8") as f:
        json.dump([item.__dict__ for item in news_list], f, indent=4, default=str)

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
    limit_news_to_proceed = 5
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
