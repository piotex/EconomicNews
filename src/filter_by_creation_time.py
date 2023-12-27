import dataclasses
import json
from datetime import datetime, timedelta
from models.model_news import NewsModel


def filter_by_date(my_class_objects, day_to_see_in_past_in_in):
    res = []
    yesterday = datetime.now() - timedelta(days=day_to_see_in_past_in_in)
    for elem in my_class_objects:
        if elem.creation_time == '':
            continue
        try:
            formatted_date = datetime.fromisoformat(elem.creation_time)
            if formatted_date.date() >= yesterday.date():
                res.append(elem)
        except Exception as exxx:
            print("=== error ===")
            print(exxx)
            print(elem)
            print("=== error ===")
            pass
    return res


def filter_by_unique_url(res):
    dict_of_model_news = {}
    for obj in res:
        if obj.url not in dict_of_model_news:
            dict_of_model_news[obj.url] = obj
    res = list(dict_of_model_news.values())

    res = [dataclasses.asdict(news) for news in res]
    return res


def filter_by_creation_time(day_to_see_in_past_in):
    print(f"filter_by_creation_time")
    path_news_list = "../data_files/important_files/news_list.json"

    with open(path_news_list, "r") as json_file:
        data_from_json = json.load(json_file)
    my_class_objects = [NewsModel(**item) for item in data_from_json]

    res = filter_by_date(my_class_objects, day_to_see_in_past_in)
    res = filter_by_unique_url(res)

    with open(path_news_list, "w") as json_file:
        json.dump(res, json_file, indent=4)


if __name__ == "__main__":
    day_to_see_in_past = 1
    filter_by_creation_time(day_to_see_in_past)
