from unicodedata import name
from PIL import Image, ImageFilter
import io

# inherite from ImageFilter module

    


def apply_filter(file: object, filter: str) -> object:
    """
    TODO:
    1. Accept the image as file object, and the filter type as string
    2. Open the as an PIL Image object
    3. Apply the filter
    4. Convert the PIL Image object to file object
    5. Return the file object
    """
    print(file)
    image = Image.open(file)
    filtered_image = image.filter(getattr(ImageFilter, filter.upper()))
    output = io.BytesIO()
    filtered_image.save(output, format="JPEG")
    output.seek(0)
    return output

def apply_custom_filter(file: object, filter: str) -> object:
    filters = {"sepia": sepia, "black_and_white": black_and_white, "invert": invert}
    return filters[filter](file)

def sepia(image_path : str)-> Image:
    img = Image.open(image_path)
    width, height = img.size
    pixels = img.load()

    for py in range(height):
        for px in range(width):
            r, g, b = pixels[px, py]
            tr = int(r * 0.393 + g * 0.769 + b * 0.189) 
            tg = int(r * 0.349 + g * 0.686 + b * 0.168)
            tb = int(r * 0.272 + g * 0.534 + b * 0.131)
            if tr > 255:
                tr = 255
            if tg > 255:
                tg = 255
            if tb > 255:
                tb = 255

            pixels[px, py] = (tr, tg, tb)

    output = io.BytesIO()
    img.save(output, format="JPEG")
    output.seek(0)
    return output

def black_and_white(image_path : str)-> Image:
    img = Image.open(image_path)
    width, height = img.size
    pixels = img.load()


    for py in range(height):
        for px in range(width):
            r, g, b = pixels[px, py]
            tr = int((r + g + b) / 3)
            tg = int((r + g + b) / 3)
            tb = int((r + g + b) / 3)
            pixels[px, py] = (tr, tg, tb)


    output = io.BytesIO()
    img.save(output, format="JPEG")
    output.seek(0)
    return output

def invert(image_path : str)-> Image:
    img = Image.open(image_path)
    width, height = img.size
    pixels = img.load()


    for py in range(height):
        for px in range(width):
            r, g, b = pixels[px, py]
            tr = 255 - r
            tg = 255 - g
            tb = 255 - b
            pixels[px, py] = (tr, tg, tb)


    output = io.BytesIO()
    img.save(output, format="JPEG")
    output.seek(0)
    return output


