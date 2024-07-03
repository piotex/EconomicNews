from dataclasses import dataclass
import json
import os
import time
from datetime import datetime


@dataclass
class NewsModel:
    idx: str = ""
    url: str = ""
    comments_count: int = -1
    article_text: str = ""
    gemini_in_text: str = ""
    gemini_out_text: str = ""

    creation_date: datetime = datetime.now()
    actualization_date: datetime = datetime.now()

    img_dir_path: str = ""
    vvt_path: str = ""
    mp3_path: str = ""


obj_list_path = "data/obj_list.json"
obj_path = "data/obj.json"


def load_obj_list() -> list[NewsModel]:
    with open(obj_list_path, "r", encoding="utf-8") as f:
        list_of_users = json.load(f)
        list_of_users = [NewsModel(**item) for item in list_of_users]
        for a in list_of_users:
            a.creation_date = datetime.strptime(str(a.creation_date), "%Y-%m-%d %H:%M:%S")
            a.actualization_date = datetime.strptime(str(a.actualization_date), "%Y-%m-%d %H:%M:%S")
    return list_of_users


def load_obj() -> NewsModel:
    with open(obj_path, "r", encoding="utf-8") as f:
        item = json.load(f)
        model = NewsModel(**item)
        model.creation_date = datetime.strptime(str(model.creation_date), "%Y-%m-%d %H:%M:%S")
        model.actualization_date = datetime.strptime(str(model.actualization_date), "%Y-%m-%d %H:%M:%S")
    return model


def save_obj_list(news_list: list[NewsModel]):
    with open(obj_list_path, "w", encoding="utf-8") as f:
        json.dump([item.__dict__ for item in news_list], f, indent=4, default=str)


def save_obj(news: NewsModel):
    with open(obj_path, "w", encoding="utf-8") as f:
        json.dump(news.__dict__, f, indent=4, default=str)
