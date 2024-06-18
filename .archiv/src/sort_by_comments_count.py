import dataclasses
import json
from models.model_news import NewsModel

MAX_COUNT = 12


def sort_by_comments_count():
    print(f"sort_by_comments_count")
    path_news_list = "../data_files/important_files/news_list.json"

    with open(path_news_list, "r") as json_file:
        data_from_json = json.load(json_file)
    my_class_objects = [NewsModel(**item) for item in data_from_json]

    # my_class_objects = sorted(my_class_objects,
    #                           key=lambda obj: obj.comments_number, reverse=True)
    my_class_objects = sorted(my_class_objects,
                              key=lambda x: (x.comments_number, len(x.quick_info)),
                              reverse=True)

    news_dict_list = [dataclasses.asdict(news) for news in my_class_objects]
    with open(path_news_list, "w") as json_file:
        json.dump(news_dict_list, json_file, indent=4)


if __name__ == "__main__":
    sort_by_comments_count()
