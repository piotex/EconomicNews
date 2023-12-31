import json
from models.model_news import NewsModel
from yt_manager_2_0 import *
import logging
import os
from datetime import date

def yt_publisher():
    print(f"yt_publisher")
    file_log_name = f'../data_files/logs/log-{str(date.today())}.log'
    if os.path.isfile(file_log_name):
        os.remove(file_log_name)
    logging.basicConfig(format='%(asctime)s-%(levelname)s-%(message)s', filename=file_log_name, level="WARN")
    logging.debug('============== App Started ==============')


    path_news_list = "../data_files/important_files/news_list.json"
    with open(path_news_list, "r") as json_file:
        data_from_json = json.load(json_file)
    my_class_objects = [NewsModel(**item) for item in data_from_json]

    path_to_usr_pwd = "../../usr_pwd.txt"
    with open(path_to_usr_pwd, "r") as file:
        res = file.readlines()
        usr = res[0].strip()
        pwd = res[1].strip()

    driver = get_init_driver()
    time.sleep(1)
    accept_cookies_youtube(driver)
    driver.maximize_window()
    time.sleep(10)
    login(driver, usr, pwd)

    filepath = "/home/pkubon/Desktop/EconomicNews/data_files/movies/final.mp4"
    filepath = "/home/pkubon/Desktop/git/EconomicNews/data_files/movies/final.mp4"
    title_tags = "#shorts #biznes"
    title = f"{my_class_objects[0].header[0:-(len(title_tags)+2)]} {title_tags}"
    description = (f"{my_class_objects[0].header} \n"
                   f"{my_class_objects[1].header} \n"
                   f"{my_class_objects[2].header} \n"
                   f"{my_class_objects[3].header} \n"
                   f"{my_class_objects[4].header} \n"
                   f"{my_class_objects[0].quick_info} \n"
                   f"{my_class_objects[1].quick_info}")
    tags = "short, shorts, biznes"
    send_video(driver_loc=driver, file_path=filepath, title=title, description=description, tags=tags)

    time.sleep(100)

if __name__ == "__main__":
    yt_publisher()