from PIL import Image, ImageOps
from tqdm import tqdm

image = Image.open("road.jpg")
image_rgb = image.convert("RGB")
image_gray = ImageOps.grayscale(image_rgb)
image_gray.show()

def naive(image_gray, mask_size):
    to_change = image_gray.copy()
    width, height = to_change.size
    pixels = to_change.load()

    smoothed_image = Image.new('L', (width, height))
    smoothed_pixels = smoothed_image.load()

    offset = mask_size // 2

    for i in tqdm(range(width)):
        for j in range(height):

            sum_val = 0
            count = 0

            for k in range(-offset, offset + 1):
                for l in range(-offset, offset + 1):
                    ni = i + k
                    nj = j + l

                    if 0 <= ni < width and 0 <= nj < height:
                        sum_val += pixels[ni, nj]
                        count += 1

            average = sum_val // count 

            smoothed_pixels[i, j] = average

    return smoothed_image

smoothed_image = naive(image_gray, 1000)
smoothed_image.show()