import cv2
import numpy as np
import random

image_1 = cv2.imread('1.jpg', cv2.IMREAD_UNCHANGED)
image_2 = cv2.imread('2.jpg', cv2.IMREAD_UNCHANGED)

width = 1080
height = 1920
frame_count = 0
fps = 25
transition_speed = 100

img1_time_s = 2
img2_time_s = 2
transition_time_s = 2
tmp_transition_time_s = height/(transition_time_s*fps)

# resize img_1 and img_2

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter('video.mp4', fourcc, fps, (width, height))

# frame = image_1                 # np.zeros((height, width, 3), np.uint8)
# for i in range(img1_time_s*fps):
#     video.write(frame)
#     frame_count += 1

frame_numb = 1
frame = image_1
random_rows = list(range(height))
random.shuffle(random_rows)
for row in range(height):
    random_row = random_rows[row]
    for column in range(width):
        cv2.circle(
            frame,  # Frame to write pixel to
            (column, random_row),  # Center coordinates of a circle
            1,  # Circle radius
            (int(image_2[random_row][column][0]), int(image_2[random_row][column][1]), int(image_2[random_row][column][2])),  # RGB
            -1  # Thickness
        )
    # Write video frame
    frame_numb += 1
    if frame_numb >= tmp_transition_time_s:
        frame_numb = 0
        frame_count += 1
        video.write(frame)

video.write(frame)

# frame = image_2
# for i in range(img2_time_s*fps):
#     video.write(frame)
#     frame_count += 1

# Release video
video.release()

# Show image in a window (optional)
# cv2.imshow('Image', frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
