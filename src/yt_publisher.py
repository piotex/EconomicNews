import time
from yt_manager_2_0 import *
from usr_pwd import *
import logging
import os
from datetime import date


def yt_publisher():
    file_log_name = f'../data_files/logs/log-{str(date.today())}.log'
    if os.path.isfile(file_log_name):
        os.remove(file_log_name)
    logging.basicConfig(format='%(asctime)s-%(levelname)s-%(message)s', filename=file_log_name, level="WARN")
    logging.debug('============== App Started ==============')


    driver = get_init_driver()
    time.sleep(1)
    accept_cookies_youtube(driver)

    time.sleep(10)

    login(driver, usr, pwd)

    filepath = "/home/pkubon/Desktop/EconomicNews/data_files/movies/final.mp4"
    title = "test title :)"
    description = "test description :D"
    tags = "tag1, tag2, ala"
    send_video(driver_loc=driver, file_path=filepath, title=title, description=description, tags=tags)

    time.sleep(1000)

if __name__ == "__main__":
    yt_publisher()