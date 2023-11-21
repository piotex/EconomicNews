import os
import subprocess
import cv2
import numpy as np
from PIL import Image

screen_path = "screen_shots"
screen_tmp_path = "screen_shots_tmp"
out_path = ""

video_width = 1080
video_height = 1920
video_fps = 30
fontScale = 2.3
font = cv2.FONT_HERSHEY_SIMPLEX


def resize_images():
    for file in os.listdir(screen_path):
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"):
            im = Image.open(os.path.join(screen_path, file))
            im_resize = im.resize((video_width, video_height), Image.NEAREST)
            im_resize.save(os.path.join(screen_tmp_path, file), 'png', quality=100)


def get_image_list():
    res = [img for img in os.listdir(screen_tmp_path)
           if img.endswith(".jpg") or
           img.endswith(".jpeg") or
           img.endswith("png")]
    return res


def insert_black_white_test_into_image(img, in_text, pos_x, pos_y):
    thickness = 30
    color = (0, 0, 0)
    text_width, text_height = cv2.getTextSize(in_text, font, fontScale, thickness)[0]
    CenterCoordinates = (int(img.shape[1] / 2) - int(text_width / 2) + pos_x,
                         int(img.shape[0] / 2) + int(text_height / 2) + pos_y)
    img = cv2.putText(img, in_text, CenterCoordinates, font, fontScale, color, thickness, cv2.LINE_AA, False)

    thickness = 8
    color = (255, 255, 255)
    img = cv2.putText(img, in_text, CenterCoordinates, font, fontScale, color, thickness, cv2.LINE_AA, False)

    return img

def add_new_line_char_to_text(text_from_json):
    result = ''
    chunk_size = 20
    tab = text_from_json.split()

    sub_str = ""
    for word in tab:
        if len(sub_str + word) > chunk_size:
            result += sub_str + "\n"
            sub_str = ""
        sub_str += word + " "
    return result


def show_image_for_x(video, img, ms_time):
    time_len = int(ms_time / video_fps)
    for i in range(0, time_len, 1):
        video.write(img)
    pass

def generate_video():
    text_from_json = "Potwierdzilismy chec wspolpracy parlamentarnej z Polska 2050, kontynuowanie Trzeciej Drogi to jest dla nas jedna z bardzo waznych uchwal przyjetych wczoraj na Radzie Naczelnej - przekazaal w niedziele dziennikarzom prezes PSL Wladyslaw Kosiniak-Kamysz."
    video_name = 'movies/my_video.avi'

    text_from_json = add_new_line_char_to_text(text_from_json)
    images = get_image_list()

    video = cv2.VideoWriter(video_name, 0, video_fps, (video_width, video_height))

    for image in images:
        for i, line in enumerate(text_from_json.split('\n')):
            img = cv2.imread(os.path.join(screen_tmp_path, image))
            img = insert_black_white_test_into_image(img, line, 0, 300)
            show_image_for_x(video, img, 100)

    #########################################################################

    cv2.destroyAllWindows()
    video.release()


resize_images()

generate_video()

# ########## working ##############################################################################

# vid_path = "movies/my_video.avi"
# audio_path = "audio/1.quick_info.mp3"
# # out_path = "movies/my_video.mp4"
# out_path = "movies/my_video_2.avi"
# command = f"ffmpeg -i {vid_path} -i {audio_path} -c copy -map 0:v:0 -map 1:a:0 {out_path}"
# subprocess.run(command, shell=True, timeout=None)

################# working #############################################################

# def convert_avi_to_mp4(avi_file_path, output_name):
#     command = f"ffmpeg -i {avi_file_path} -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 {output_name}"
#     subprocess.run(command, shell=True, timeout=None)
#     return True
#
#
# convert_avi_to_mp4("movies/my_video.avi", "movies/my_video.mp4")

####################################################################################################
