from moviepy.editor import VideoFileClip, AudioFileClip

sciezka_gif = "movies/animacja_z_napisem.gif"
sciezka_muzyki = 'audio/1.quick_info.mp3'
sciezka_wyjsciowa = "movies/fimal.mp4"

clip_gif = VideoFileClip(sciezka_gif)
audio = AudioFileClip(sciezka_muzyki)

film_z_muzyka = clip_gif.set_audio(audio)

film_z_muzyka.write_videofile(sciezka_wyjsciowa, codec='libx264', audio_codec='aac')
