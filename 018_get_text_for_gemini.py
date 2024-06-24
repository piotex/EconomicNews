import json
import os
import time
from dataclasses import dataclass
from datetime import datetime
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

obj_list_path = "data/obj_list.json"


@dataclass
class NewsModel:
    idx: str = ""
    url: str = ""
    comments_count: int = -1
    article_text: str = ""

    creation_date: datetime = datetime.now()
    actualization_date: datetime = datetime.now()

    img_dir_path: str = ""
    vvt_path: str = ""
    mp3_path: str = ""


def load_obj_list() -> list[NewsModel]:
    with open(obj_list_path, "r") as f:
        list_of_users = json.load(f)
        list_of_users = [NewsModel(**item) for item in list_of_users]
        for a in list_of_users:
            a.actualization_date = datetime.strptime(str(a.actualization_date), "%Y-%m-%d %H:%M:%S")
    return list_of_users



def save_obj_list(news_list: list[NewsModel]):
    with open(obj_list_path, "w", encoding="utf-8") as f:
        json.dump([item.__dict__ for item in news_list], f, indent=4, default=str)


def main():
    obj_list = load_obj_list()

    txt = """
Streść poniższy artykuł, tak, żeby dobrze się tego słuchało na TikTok.
Chcę, żebyś wybrał najciekawsze wątki z całego materiału i podsumował je w angażujący sposób do 5 zdań maksymalnie.
Unikaj zbędnych przymiotników.
Przedstaw poniższe informacje w rzetelny, obiektywny i angażujący widza TikToka sposób. 
    """

    with open(f"data/text_for_gemini/{obj_list[0].idx}.txt", "w", encoding="utf-8") as f:
        f.write(txt+obj_list[0].article_text)

    print("""
Czekam na twoją akcje...
Skopiuj tekst z data/text_for_gemini
Uruchom polecenie w gemini
Zapisz w tym samym pliku rezultat wygenerowany przez gemini
Po zapisaniu wciśnij ENTER w konsoli
""")
    a = input()

    with open(f"data/text_for_gemini/{obj_list[0].idx}.txt", "r", encoding="utf-8") as f:
        obj_list[0].article_text = f.read()

    save_obj_list(obj_list)


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
