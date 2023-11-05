import dataclasses
import json
from datetime import datetime, timedelta

from models.model_news import model_news

file_path = "important_files/1_get_raw_info.json"

with open(file_path, "r") as json_file:
    data_from_json = json.load(json_file)

my_class_objects = [model_news(**item) for item in data_from_json]

yesterday = datetime.now() - timedelta(days=1)

res = []
for elem in my_class_objects:
    try:
        formatted_date = datetime.fromisoformat(elem.creation_time)
        if formatted_date.date() >= yesterday.date():
            res.append(elem)
    except Exception as exxx:
        pass

dict_of_model_news = {}
for obj in res:
    if obj.url not in dict_of_model_news:
        dict_of_model_news[obj.url] = obj
res = list(dict_of_model_news.values())

file_path = "important_files/2_filter_by_creation_time.json"
res = [dataclasses.asdict(news) for news in res]
with open(file_path, "w") as json_file:
    json.dump(res, json_file, indent=4)
