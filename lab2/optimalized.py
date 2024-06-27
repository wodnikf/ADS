from PIL import Image, ImageOps
import numpy as np
from tqdm import tqdm

class Summed_Area_Table:
    def __init__(self, size, data):
        width, height = size

        self.size = size
        self.data = data
        self.memo = [None for _ in range(width * height)]
        self.generate()

    def generate(self):
        width, height = self.size
        self.memo = [self.get(x, y) for y in range(height) for x in range(width)]

    def get(self, x, y):
        width, height = self.size
        index = y * width + x
        if x < 0 or y < 0:
            return 0
        elif self.memo[index] is not None:
            return self.memo[index]
        else:
            calc = self.get(x - 1, y) + self.get(x, y - 1) - self.get(x - 1, y - 1) + self.data[index]
            self.memo[index] = calc
            return calc

    def total(self, x0, y0, x1, y1):
        a = self.get(x0 - 1, y0 - 1)
        b = self.get(x0 - 1, y1)
        c = self.get(x1, y0 - 1)
        d = self.get(x1, y1)
        return d + a - b - c


def apply_mean_filter(image, mask_size):
    width, height = image.size
    pixels = np.array(image)
    
    sat = Summed_Area_Table(size=(width, height), data=pixels.flatten())

    filtered_image = np.zeros_like(pixels)
    
    offset = mask_size // 2

    for y in tqdm(range(height)):
        for x in range(width):
            x0 = max(0, x - offset)
            y0 = max(0, y - offset)
            x1 = min(width - 1, x + offset)
            y1 = min(height - 1, y + offset)
            
            area = (x1 - x0 + 1) * (y1 - y0 + 1)
            filtered_image[y, x] = sat.total(x0, y0, x1, y1) // area

    return Image.fromarray(filtered_image)


image = Image.open("road.jpg")
image_gray = ImageOps.grayscale(image)

mask_size = 81
filtered_image = apply_mean_filter(image_gray, mask_size)

filtered_image.show()
