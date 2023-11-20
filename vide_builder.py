import os
import subprocess
import cv2
import numpy as np
from PIL import Image

screen_path = "screen_shots"
screen_tmp_path = "screen_shots_tmp"
out_path = ""

mean_width = 1080
mean_height = 1920

for file in os.listdir(screen_path):
    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"):
        im = Image.open(os.path.join(screen_path, file))
        imResize = im.resize((mean_width, mean_height), Image.NEAREST)
        imResize.save(os.path.join(screen_tmp_path, file), 'png', quality=100)


def generate_video():
    video_name = 'movies/my_video.avi'

    images = [img for img in os.listdir(screen_tmp_path)
              if img.endswith(".jpg") or
              img.endswith(".jpeg") or
              img.endswith("png")]

    frame = cv2.imread(os.path.join(screen_tmp_path, images[0]))

    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, 0, 1, (width, height))

    for image in images:
        img = cv2.imread(os.path.join(screen_tmp_path, image))

        window_name = 'Image'
        text = 'GeeksforGeeks'
        text = "Potwierdzilismy chec"
        text = "wspolpracy parlamentarnej z Polska 2050, kontynuowanie Trzeciej Drogi to jest dla nas jedna z bardzo waznych uchwal przyjetych wczoraj na Radzie Naczelnej - przekazaal w niedziele dziennikarzom prezes PSL Wladyslaw Kosiniak-Kamysz."
        result = ''
        chunk_size = 20
        for i in range(0, len(text), chunk_size):
            result += text[i:i + chunk_size] + '\n'
        text = result

        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (0, 185)
        # org = (1080/2, 1920/2)


        y0, dy = 50, 65
        for i, line in enumerate(text.split('\n')):
            y = y0 + i * dy
            fontScale = 3
            thickness = 30
            color = (0, 0, 0)
            img = cv2.putText(img, line, (0, y), font, fontScale, color, thickness, cv2.LINE_AA, False)
            fontScale = 3
            thickness = 8
            color = (255, 255, 255)
            img = cv2.putText(img, line, (0, y), font, fontScale, color, thickness, cv2.LINE_AA, False)
            video.write(img)







#########################################################################

    cv2.destroyAllWindows()
    video.release()


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

