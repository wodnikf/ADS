from PIL import Image
import matplotlib.pyplot as plt

image = Image.open("yoda.jpeg")
image_rgb = image.convert("RGB")

all_pixels = image.size[0] * image.size[1]

def grayscale(image):
    grayscale_image = Image.new("L", image.size)

    for x in range(image.width):
        for y in range(image.height):
            
            r, g, b = image.getpixel((x, y))

            luminance = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

            grayscale_image.putpixel((x, y), luminance)

    return grayscale_image

def pixel_apperances(image):
    pixel_counts = [0] * 256
    
    for x in range(image.width):
        for y in range(image.height):
            pixel_value = image.getpixel((x, y))
            pixel_counts[pixel_value] += 1
        
    return pixel_counts

def probability(pixel_counts, all_pixels):
    prob = [0] * 256
    for intensity in range(256):
        prob[intensity] = pixel_counts[intensity] / all_pixels

    return prob


def cdf_calc(prob):
    cdf = [0] * 256
    for i in range(256):
        if i == 0:
            cdf[i] = prob[0]
        else:
            cdf[i] = cdf[i - 1] + prob[i]

    return cdf

def level_times_cdf(cdf):
    level = [0] * 256
    
    for i in range(256):
        level[i] = i * cdf[i]

    return level


def rounding(level):
    for i in range(256):
        level[i] = round(level[i])

    return level

def histogram_equalize(image):
    grayscale_image = image.convert("L")
    
    pixel_counts = pixel_apperances(grayscale_image)
    
    prob = probability(pixel_counts, all_pixels)
    
    cdf = cdf_calc(prob)
    
    equalized_image = Image.new("L", grayscale_image.size)
    for x in range(grayscale_image.size[0]):
        for y in range(grayscale_image.size[1]):
            pixel_value = grayscale_image.getpixel((x, y))
            new_pixel_value = int(round(255 * cdf[pixel_value]))
            equalized_image.putpixel((x, y), new_pixel_value)
    
    return equalized_image


grayscale_image = grayscale(image)
grayscale_image.show()
new_image = histogram_equalize(grayscale_image)
new_image.show()
