import dataclasses
import json
from models.model_news import model_news
from yt_manager_2_0 import *


def get_val_from_attributes_list(key: str, attrs_list) -> str:
    res_list = [sub_list for sub_list in attrs_list if sub_list and sub_list[0] == key]
    res_elem = res_list[0][1]
    return res_elem


file_path = "bankier_url/bakier_url_format_1.txt"
with open(file_path, 'r') as file:
    lines = file.readlines()

url = lines[0]

driver = get_init_driver()
time.sleep(1)
driver.get(url)
time.sleep(1)

file_path = "important_files/1_get_raw_info.json"
list_of_model_news = []
with open(file_path, "w") as json_file:
    for i in range(2, 23, 1):
        try:
            x_path = f"/html/body/div[3]/div[1]/div[2]/div[1]/section/div[{i}]/div/div/time"
            attrs_list = []
            logo = driver.find_element(by=By.XPATH, value=x_path)
            for attr in logo.get_property('attributes'):
                attrs_list.append([attr['name'], attr['value']])
            tmp_creation_time = get_val_from_attributes_list("datetime", attrs_list)

            x_path = f"/html/body/div[3]/div[1]/div[2]/div[1]/section/div[{i}]/div/span/a"
            attrs_list = []
            logo = driver.find_element(by=By.XPATH, value=x_path)
            for attr in logo.get_property('attributes'):
                attrs_list.append([attr['name'], attr['value']])
            tmp_url = get_val_from_attributes_list("href", attrs_list)
            tmp_header = f"https://www.bankier.pl/{get_val_from_attributes_list('title', attrs_list)}"

            model = model_news(
                url=tmp_url,
                header=tmp_header,
                creation_time=tmp_creation_time
            )
            list_of_model_news.append(model)
        except Exception as exxx:
            list_of_model_news.append(model_news(comments_number=i))
            pass

    news_dict_list = [dataclasses.asdict(news) for news in list_of_model_news]
    json.dump(news_dict_list, json_file, indent=4)
