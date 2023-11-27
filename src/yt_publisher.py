import time
from yt_manager_2_0 import *
from usr_pwd import *

if __name__ == "__main__":
    driver = get_init_driver()
    time.sleep(1)
    accept_cookies_youtube(driver)

    time.sleep(10)

    login(driver, usr, pwd)

    filepath = "/home/pkubon/Downloads/2.mp4"
    title = "test title :)"
    description = "test description :D"
    tags = "tag1, tag2, ala"
    send_video(driver_loc=driver, file_path=filepath, title=title, description=description, tags=tags)

    time.sleep(1000)