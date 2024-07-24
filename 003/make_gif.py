import glob
import sys
import logging
from PIL import Image
import numpy as np
from datetime import datetime
import imageio.v2 as imageio

DURATION = 1.5
VALID_EXTENSIONS = ('png', 'jpeg', 'jpg')

def get_current_timestamp():
    """Generate a unique timestamp."""
    return datetime.now().strftime('%Y%m%d%H%M%S')

def resize_images_to_same_size(images):
    """Resize all images to the size of the first image."""
    target_size = images[0].size
    return [image.resize(target_size, Image.LANCZOS) for image in images]
 
def convert_images_to_numpy_arrays(images):
    """Convert a list of PIL Images to a list of NumPy arrays."""
    return [np.array(image) for image in images]

def save_as_gif(images, gif_filename, duration=DURATION):
    """Save a list of images as a GIF with specified duration."""
    imageio.mimsave(gif_filename, images, duration=[duration] * len(images), loop=0)

def validate_file_extensions(filenames):
    """Check if all filenames have valid extensions."""
    return all(f.lower().endswith(VALID_EXTENSIONS) for f in filenames)

def main():
    script_name = sys.argv.pop(0)
    arguments = sys.argv

    if not arguments:
        print(f'Usage: {script_name} <glob pattern or list of images>')
        sys.exit(1)

    filenames = arguments if len(arguments) > 1 else glob.glob(arguments[0])
    filenames = [f for f in filenames if validate_file_extensions([f])]

    if not filenames:
        print('No valid files found.')
        sys.exit(1)

    images = [Image.open(f) for f in filenames]
    resized_images = resize_images_to_same_size(images)
    numpy_images = convert_images_to_numpy_arrays(resized_images)
    gif_filename = f'out_{get_current_timestamp()}.gif'
    save_as_gif(numpy_images, gif_filename)

if __name__ == "__main__":
    main()
