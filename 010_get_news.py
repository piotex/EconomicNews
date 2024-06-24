import json
import os
import random
import shutil
import time
from typing import List

from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta, date
from dataclasses import dataclass


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


main_url = "https://www.bankier.pl"
obj_list_path = "data/obj_list.json"
bankier_urls = [
    "https://bankier.pl/rynki/wiadomosci",
    "https://www.bankier.pl/gielda/wiadomosci",
    "https://www.bankier.pl/fundusze/wiadomosci",
    "https://www.bankier.pl/gielda/wiadomosci/komunikaty-spolek",
    "https://www.bankier.pl/gospodarka/analizy",
    "https://www.bankier.pl/gospodarka/wiadomosci",
    "https://www.bankier.pl/surowce/wiadomosci",
    "https://www.bankier.pl/gielda/wiadomosci/wywiady-ze-spolek",
    "https://www.bankier.pl/waluty/wiadomosci",
]


def init_folders():
    print(f"init_folders")
    data_files = 'data'
    folders = [
        'audio',
        'gifs',
        'important_files',
        'movies',
        'screen_shots',
        'text_for_gemini',
        'logs'
    ]
    for folder in folders:
        sciezka_folderu = os.path.join(data_files, folder)
        if os.path.exists(sciezka_folderu):
            shutil.rmtree(sciezka_folderu)
        os.makedirs(os.path.join(data_files, folder))


def get_obj_from_main_site(url: str) -> list[NewsModel]:
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        articles = soup.find_all("div", class_="article")
        result = []
        for article in articles:
            href = article.find("a")["href"] if article.find("a") else None
            creation_date = datetime.strptime(article.find_all("time")[0]["datetime"][:-6], "%Y-%m-%dT%H:%M:%S")
            actualization_date = datetime.strptime(article.find_all("time")[1]["datetime"][:-6], "%Y-%m-%dT%H:%M:%S") if len(article.find_all("time")) > 1 else datetime(1901, 1, 1)
            result.append(NewsModel(idx=href.split("/")[-1].split(".")[0][:50] ,url=main_url + href, creation_date=creation_date, actualization_date=actualization_date))
        return result
    raise Exception(f"Other response code: {response.status_code} \n\n message: {response.text}")


def get_valid_obj_from_home_page(news_list: list[NewsModel]) -> list[NewsModel]:
    date_to_compare = datetime.now() - timedelta(days=1)
    return [x for x in news_list if x.creation_date > date_to_compare]


def get_todays_obj_list() -> list[NewsModel]:
    main_list_of_obj = []
    for idx, url in enumerate(bankier_urls):
        print(f"{idx + 1} / {len(bankier_urls)}", end="\r")
        for i in range(1, 5, 1):
            time.sleep(random.uniform(1.0, 1.5))
            list_of_obj = get_obj_from_main_site(f"{url}/{i}")
            list_of_obj = get_valid_obj_from_home_page(list_of_obj)
            main_list_of_obj += list_of_obj
            if len(list_of_obj) < 15:
                break
    print("")
    return main_list_of_obj


def save_obj_list(news_list: list[NewsModel]):
    with open(obj_list_path, "w", encoding="utf-8") as f:
        json.dump([item.__dict__ for item in news_list], f, indent=4, default=str)


def load_obj_list() -> list[NewsModel]:
    with open(obj_list_path, "r") as f:
        list_of_users = json.load(f)
        list_of_users = [NewsModel(**item) for item in list_of_users]
        for a in list_of_users:
            a.creation_date = datetime.strptime(str(a.creation_date), "%Y-%m-%d %H:%M:%S")
            a.actualization_date = datetime.strptime(str(a.actualization_date), "%Y-%m-%d %H:%M:%S")
    return list_of_users


def get_obj_from_news_page(url: str) -> NewsModel:
    mandatory_txt = "Komentarze"
    response = requests.get(url)
    if response.status_code == 200:
        comments_count = -1
        html_content = response.text
        in_text = BeautifulSoup(html_content, "html.parser").find_all("section", class_='o-article-content')[-1].text
        try:
            comment_txt = BeautifulSoup(html_content, "html.parser").find_all("h3")[-1].text
            comments_count = int(
                comment_txt.split("(")[-1].replace(")", "").strip()) if mandatory_txt in comment_txt else -1
        except:
            pass
        return NewsModel(url=url, comments_count=comments_count, article_text=in_text)
    raise Exception("=== idk why 4638546854 ===")


def sort_obj_list_by_comments(news_model_list: list[NewsModel]) -> list[NewsModel]:
    return sorted(news_model_list, key=lambda model: model.comments_count, reverse=True)


def main():
    init_folders()
    main_list_of_obj = get_todays_obj_list()
    for idx, obj1 in enumerate(main_list_of_obj):
        print(f"{idx + 1} / {len(main_list_of_obj)}", end="\r")
        tmp_obj = get_obj_from_news_page(obj1.url)
        obj1.comments_count = tmp_obj.comments_count
        obj1.article_text = tmp_obj.article_text
        save_obj_list(main_list_of_obj)
        time.sleep(random.uniform(1.0, 1.5))
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

    # resp_obj = get_data_from_page()

    # get_raw_info()
    #
    # filter_by_creation_time()
    #
    # start_elem = 1
    # get_comments_count(start_elem)
    # sort_by_comments_count()
    # # limit_resp()
    # save_pd_notion_files()

    #
    #
    #
    #
    # ==============================
    # start = 4
    # end = start+1
    # for i in range(start, end):
    #     text_to_speech(i)
    #     gif_builder(i)
    #
    # for i in range(5):
    #     video_builder(i)
    #
    # video_merge()
    # yt_publisher()
