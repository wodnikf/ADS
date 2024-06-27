from PIL import Image

image = Image.open("yoda.jpeg")
image_rgb = image.convert("RGB")

def bw_one_t(image_rgb):
    threshold = 100
    to_change = image_rgb.copy()
    for i in range(to_change.size[0]):
        for j in range(to_change.size[1]):
            r, g, b = to_change.getpixel((i, j))
            average = (r + g + b) / 3
            if average <= threshold:
                to_change.putpixel((i, j), (0, 0, 0))
            else:
                to_change.putpixel((i, j), (255, 255, 255))
    to_change.show()

bw_one_t(image_rgb)

def bw_two_t(image_rgb):
    threshold_1 = 100
    threshold_2 = 200
    to_change = image_rgb.copy()
    for i in range(to_change.size[0]):
        for j in range(to_change.size[1]):
            r, g, b = to_change.getpixel((i, j))
            average = (r + g + b) / 3
            if average <= threshold_1 or average >= threshold_2:
                to_change.putpixel((i, j), (0, 0, 0))
            else:
                to_change.putpixel((i, j), (255, 255, 255))
    to_change.show()

bw_two_t(image_rgb)