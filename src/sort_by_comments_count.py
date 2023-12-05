import dataclasses
import json
from models.model_news import NewsModel


def sort_by_comments_count():
    print(f"sort_by_comments_count")
    path_news_list = "../data_files/important_files/news_list.json"

    with open(path_news_list, "r") as json_file:
        data_from_json = json.load(json_file)
    my_class_objects = [NewsModel(**item) for item in data_from_json]

    for elem in my_class_objects:
        elem.header = elem.header.replace("\"", "")
        elem.quick_info = elem.quick_info.replace("\"", "")
        elem.quick_info = elem.quick_info.replace(",", "")
        elem.quick_info = elem.quick_info.replace("...", "")

    my_class_objects = sorted(my_class_objects, key=lambda obj: obj.comments_number, reverse=True)
    my_class_objects = my_class_objects[:5]

    news_dict_list = [dataclasses.asdict(news) for news in my_class_objects]
    with open(path_news_list, "w") as json_file:
        json.dump(news_dict_list, json_file, indent=4)


if __name__ == "__main__":
    sort_by_comments_count()
