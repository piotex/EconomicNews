import dataclasses
import json
from models.model_news import model_news
from yt_manager_2_0 import *


def get_val_from_attributes_list(key: str, attrs_list) -> str:
    res_list = [sub_list for sub_list in attrs_list if sub_list and sub_list[0] == key]
    res_elem = res_list[0][1]
    return res_elem


def get_creation_time(driver_in, i):
    attrs_list = []
    x_path = f"/html/body/div[3]/div[1]/div[2]/div[1]/section/div[{i}]/div/div/time"
    logo = driver_in.find_element(by=By.XPATH, value=x_path)
    for attr in logo.get_property('attributes'):
        attrs_list.append([attr['name'], attr['value']])
    tmp_creation_time_1 = get_val_from_attributes_list("datetime", attrs_list)
    return tmp_creation_time_1


def get_url_and_header(driver_in, i):
    x_path = f"/html/body/div[3]/div[1]/div[2]/div[1]/section/div[{i}]/div/span/a"
    attrs_list = []
    logo = driver_in.find_element(by=By.XPATH, value=x_path)
    for attr in logo.get_property('attributes'):
        attrs_list.append([attr['name'], attr['value']])
    tmp_url_1 = f"https://www.bankier.pl{get_val_from_attributes_list('href', attrs_list)}"
    tmp_header_1 = get_val_from_attributes_list('title', attrs_list)
    return [tmp_url_1, tmp_header_1]


path_with_urls = "bankier_url/bakier_url_format_1.txt"
path_1_get_raw_info = "important_files/1_get_raw_info.json"
list_of_model_news = []
driver = get_init_driver()
time.sleep(1)

with open(path_with_urls, 'r') as file:
    lines = file.readlines()

for url in lines:
    driver.get(url)
    time.sleep(1)
    for i in range(2, 23, 1):
        try:
            tmp_creation_time = get_creation_time(driver, i)
            tmp_url = get_url_and_header(driver, i)[0]
            tmp_header = get_url_and_header(driver, i)[1]

            model = model_news(url=tmp_url, header=tmp_header, creation_time=tmp_creation_time)
            list_of_model_news.append(model)
        except Exception as exxx:
            list_of_model_news.append(model_news(comments_number=i*(-1)))
            pass

news_dict_list = [dataclasses.asdict(news) for news in list_of_model_news]
with open(path_1_get_raw_info, "w") as json_file:
    json.dump(news_dict_list, json_file, indent=4)
