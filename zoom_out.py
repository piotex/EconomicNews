import os
from PIL import Image


def generate_zoompan(
        input_filename,
        output_filename,
        duration,
        frame_rate,
        initial_zoom,
        initial_x,
        initial_y,
        final_zoom,
        final_x,
        final_y,
):
    image = Image.open(input_filename)

    for i in range(duration):
        # the factor that we use to interpolate between the initial and final values
        interpolation_factor = i / duration

        # calculate the zoom level
        zoom_level = (1 - interpolation_factor) * initial_zoom + interpolation_factor * final_zoom

        # calculate the crop size
        crop_width = image.width / zoom_level
        crop_height = image.height / zoom_level

        # calculate the crop position
        crop_x = (image.width - crop_width) * ((1 - interpolation_factor) * initial_x + interpolation_factor * final_x)
        crop_y = (image.height - crop_height) * ((1 - interpolation_factor) * initial_y + interpolation_factor * final_y)

        # crop the image
        cropped_image = image.crop((crop_x, crop_y, crop_x + crop_width, crop_y + crop_height))

        # resize the image
        resized_image = cropped_image.resize((image.width, image.height))

        # save the image
        filename = f'{output_filename}-{i}.png'
        # make sure that the output directory exists
        parent_folder = os.path.dirname(filename)
        os.makedirs(parent_folder, exist_ok=True)

        resized_image.save(filename)

    cmd = f"ffmpeg -y -i {output_filename}-%d.png -framerate {frame_rate} {output_filename} -loglevel quiet".strip()
    os.system(cmd)

generate_zoompan("screen_shots/1.png", "movies/tmp/test.avi", 100, 30, 2, 0, 0, 1, 0, 0)