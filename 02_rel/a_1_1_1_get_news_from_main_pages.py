import random
from datetime import timedelta
import time
import requests
from bs4 import BeautifulSoup, ResultSet
from news_model import *

main_url = "https://www.bankier.pl"
obj_list_path = "data/obj_list.json"
hours = 24
max_date_in_past = datetime.now() - timedelta(hours=hours)
max_sub_sites = 5


def get_articles_from_main_site(url: str) -> ResultSet:
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Site not accessible: {response.status_code} \n\n message: {response.text}")

    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.find_all("div", class_="article")


def get_obj_from_main_site(url: str) -> list[NewsModel]:
    date_format = "%Y-%m-%dT%H:%M:%S"
    articles = get_articles_from_main_site(url)
    result = []
    for article in articles:
        href = article.find("a")["href"] if article.find("a") else None
        tmp_art_time = article.find_all("time")
        creation_date = datetime.strptime(tmp_art_time[0]["datetime"][:-6], date_format)
        actualization_date = datetime.strptime(tmp_art_time[1]["datetime"][:-6], date_format) if len(tmp_art_time) > 1 else creation_date

        model = NewsModel(
            idx=href.split("/")[-1].split(".")[0][:50],
            url=main_url + href,
            creation_date=creation_date,
            actualization_date=actualization_date
        )
        result.append(model)
    return result


def get_urls() -> list[str]:
    with open("data/urls/bankier_urls.txt", 'r', encoding="utf-8") as f:
        lines = f.readlines()
        return [l.strip().replace('\n', '') for l in lines]


def main():
    urls = get_urls()
    result = []
    for idx, url in enumerate(urls):
        for i in range(1, max_sub_sites, 1):
            print(f"{idx + 1}-{i} / {len(urls)}", end="\r")
            time.sleep(random.uniform(1.0, 1.5))

            tmp_result = get_obj_from_main_site(f"{url}/{i}")
            if len(tmp_result) < 1:
                break

            for model in tmp_result:
                if model.creation_date >= max_date_in_past:
                    result.append(model)

            save_obj_list(result)
            if tmp_result[-1].creation_date < max_date_in_past:
                break


    print(f"Total: {len(result)}", end="\n")


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
