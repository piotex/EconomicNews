import dataclasses
import json
import re

from models.model_news import model_news
from yt_manager_2_0 import *


def get_val_from_attributes_list(key: str, attrs_list) -> str:
    res_list = [sub_list for sub_list in attrs_list if sub_list and sub_list[0] == key]
    res_elem = res_list[0][1]
    return res_elem


def get_comment_count(driver_in):
    for j in range(1, 4, 1):
        try:
            x_path = f"/html/body/div[1]/div[{j}]/main/section[2]/header/h3"
            kom_text = driver_in.find_element(by=By.XPATH, value=x_path).text
            pattern = r'Komentarze \((\d+)\)'
            match = re.search(pattern, kom_text)
            res = int(match.group(1))
            return res
        except Exception as exx:
            pass
    raise Exception("==== comment_count info not found ====")



def get_quick_desc(driver_in):
    for j in range(1, 4, 1):
        try:
            x_path = f"/html/body/div[1]/div[{j}]/main/article/section/p[1]/span"
            kom_text = driver_in.find_element(by=By.XPATH, value=x_path).text
            return kom_text
        except Exception as exx:
            pass
    raise Exception("==== Quick info not found ====")


path_with_urls = "important_files/2_filter_by_creation_time.json"
path_3_get_comments_count = "important_files/3_get_comments_count.json"

with open(path_with_urls, "r") as json_file:
    data_from_json = json.load(json_file)
my_class_objects = [model_news(**item) for item in data_from_json]
driver = get_init_driver()
time.sleep(1)

i = 1
for elem in my_class_objects:
    try:
        driver.get(elem.url)
        time.sleep(1)

        elem.comments_number = get_comment_count(driver)
        elem.quick_info = get_quick_desc(driver)

        img_path = f"screen_shots/{i}.png"
        scroll_to_xxx(driver, 400)
        driver.save_screenshot(img_path)
        elem.screen_path = img_path
        i += 1
    except Exception as exxx:
        elem.comments_number = i * (-1)
        pass

    break

news_dict_list = [dataclasses.asdict(news) for news in my_class_objects]
with open(path_3_get_comments_count, "w") as json_file:
    json.dump(news_dict_list, json_file, indent=4)
