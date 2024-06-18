import dataclasses
import json
from models.model_news import NewsModel
from a_data import MAX_ARTICLE_IN_NOTION, NOTION_SENTENCE


def save_pd_notion_files():
    print(f"sort_by_comments_count")
    path_news_list = "../data_files/important_files/news_list.json"

    with open(path_news_list, "r") as json_file:
        data_from_json = json.load(json_file)
    my_class_objects = [NewsModel(**item) for item in data_from_json]

    main_sub_list = [
        my_class_objects[i:i + MAX_ARTICLE_IN_NOTION]
        for i in range(0, len(my_class_objects), MAX_ARTICLE_IN_NOTION)
    ]

    for i, sub_list in enumerate(main_sub_list):
        tekst = ""
        tekst += NOTION_SENTENCE + "\n\n"
        for my_obj in sub_list:
            tekst += f"{my_obj.header}\n"
            tekst += f"{my_obj.quick_info}\n\n"

        nazwa_pliku = f"../data_files/important_files/top_x_notion_{i}.txt"
        with open(nazwa_pliku, 'w') as plik:
            plik.write(tekst)


if __name__ == "__main__":
    save_pd_notion_files()
