import dataclasses
import json
from models.model_news import NewsModel


def save_pd_notion_files():
    print(f"sort_by_comments_count")
    path_news_list = "../data_files/important_files/news_list.json"

    with open(path_news_list, "r") as json_file:
        data_from_json = json.load(json_file)
    my_class_objects = [NewsModel(**item) for item in data_from_json]

    tekst = ""
    tekst += """Streść poniższy artykuł, tak, żeby dobrze się tego słuchało na TikTok.
Chcę, żebyś wybrał najciekawsze wątki z całego materiału i podsumował je w angażujący sposób do 5 zdań maksymalnie.
Unikaj zbędnych przymiotników.
Przedstaw poniższe informacje w rzetelny, obiektywny i angażujący widza TikToka sposób."""
    tekst += "\n\n"
    for my_obj in my_class_objects:
        tekst += f"{my_obj.header}\n"
        tekst += f"{my_obj.quick_info}\n\n"

    nazwa_pliku = f"../data_files/top_x_notion.txt"
    with open(nazwa_pliku, 'w') as plik:
        plik.write(tekst)


if __name__ == "__main__":
    save_pd_notion_files()
