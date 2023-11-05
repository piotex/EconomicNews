import dataclasses
import json
from models.model_news import model_news

path_with_urls = "important_files/3_get_comments_count.json"
path_3_get_comments_count = "important_files/4_sort_by_comments_count.json"

with open(path_with_urls, "r") as json_file:
    data_from_json = json.load(json_file)
my_class_objects = [model_news(**item) for item in data_from_json]

my_class_objects = sorted(my_class_objects, key=lambda obj: obj.comments_number, reverse=True)

news_dict_list = [dataclasses.asdict(news) for news in my_class_objects]
with open(path_3_get_comments_count, "w") as json_file:
    json.dump(news_dict_list, json_file, indent=4)

