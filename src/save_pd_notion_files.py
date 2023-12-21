import dataclasses
import json
from models.model_news import NewsModel

MAX_COUNT = 12

def save_pd_notion_files():
    print(f"sort_by_comments_count")
    path_news_list = "../data_files/important_files/news_list.json"

    with open(path_news_list, "r") as json_file:
        data_from_json = json.load(json_file)
    my_class_objects = [NewsModel(**item) for item in data_from_json]

    tekst = ""
    for my_obj in my_class_objects:
        tekst += "======================================================\n"
        tekst += "========= Comments  =========\n"
        tekst += f"{my_obj.comments_number}\n\n"
        tekst += "========= URL =========\n"
        tekst += f"{my_obj.url}\n\n"
        tekst += "========= Tytuł =========\n"
        tekst += f"{my_obj.header}\n\n"
        tekst += "========= Treść =========\n"
        tekst += f"{my_obj.quick_info}\n\n"

    nazwa_pliku = f"../data_files/important_files/top_x_notion.txt"
    with open(nazwa_pliku, 'w') as plik:
        plik.write(tekst)




if __name__ == "__main__":
    save_pd_notion_files()
