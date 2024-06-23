from moviepy.editor import *

# https://moviepy.readthedocs.io/en/latest/ref/VideoClip/VideoClip.html#videofileclip
# https://www.geeksforgeeks.org/moviepy-inserting-text-in-the-video/

length = 3
width = 1080
height = 1920

background_clip = VideoFileClip('3.mp4').subclip(0, length)
main_clip = VideoFileClip('1.mp4')

from moviepy.editor import *
txt_clip = TextClip("GeeksforGeeks", fontsize=75, color='black')
txt_clip = txt_clip.set_pos('center').set_duration(10)


background_clip = background_clip.resize((width,height))
main_clip = main_clip.resize((width/2,height/2))
main_clip = main_clip.set_position((500,500))

# combined = clips_array([[clip1, clip2]])
# # combined = combined.resize((1920,1080))
# # combined = combined.crop(x1=1166.6, y1=0, x2=2246.6, y2=1920)
# combined.write_videofile('test.mp4')

video = CompositeVideoClip([background_clip,main_clip,txt_clip], size=(width,height))
video.write_videofile('4.mp4')