import random
from bs4 import BeautifulSoup
import requests
from news_model import *

obj_list_path = "data/obj_list.json"


def update_model_from_news_page(model: NewsModel) -> NewsModel:
    response = requests.get(model.url)
    if response.status_code != 200:
        raise Exception(f"Site not accessible: {response.status_code} \n\n message: {response.text}")

    model.article_text = BeautifulSoup(response.text, "html.parser").find_all("section", class_='o-article-content')[-1].text
    try:
        comment_txt = BeautifulSoup(response.text, "html.parser").find_all("h3")[-1].text
        model.comments_count = int(comment_txt.split("(")[-1].replace(")", "").strip()) if "Komentarze" in comment_txt else -1
    except:
        pass
    return model


def sort_obj_list_by_comments(news_model_list: list[NewsModel]) -> list[NewsModel]:
    return sorted(news_model_list, key=lambda model: model.comments_count, reverse=True)


def main():
    main_list_of_obj = load_obj_list()
    for idx, model in enumerate(main_list_of_obj):
        print(f"{idx + 1} / {len(main_list_of_obj)}", end="\r")
        time.sleep(random.uniform(1.0, 1.5))

        model = update_model_from_news_page(model)
        save_obj_list(main_list_of_obj)

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
