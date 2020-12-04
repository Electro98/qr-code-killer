
import math

from PIL import Image, ImageDraw


def coordinate(index, radius, num = 100) -> (int, int):
    
    angle = math.pi/num
    x = math.cos(angle*index)*radius
    y = math.sin(angle*index)*radius
    return x, y

def new_canvas():
    """Create new canvas"""

    img = Image.new("RGB", (600, 600), "white")
    # создание белого квадрата

    name_canvas = "blank_canvas.jpg"
    img.save(name_canvas)
    # сохранение холста


def circle(name_canvas):
    """Create some circles"""

    img = Image.open(name_canvas)
    width, height = img.size
    center = (width // 2, height // 2)
    radius = width // 2
    # радиус и центр на будущее

    pixels = img.load()
    # считывание всех пикселей

    draw_circle = ImageDraw.Draw(img)
    draw_circle.ellipse((0, 0, width, height), fill = "black")
    draw_circle.ellipse((5, 5, width - 5, width - 5), fill = "white")
    draw_circle.ellipse((25, 25, width - 25, width - 25), fill = "black")
    draw_circle.ellipse((30, 30, width - 30, width - 30), fill = "white")
    
    img.save("circle_circle1.jpg", "JPEG", quality=100)
    # сохранение картинки с кругами 


def sector(name_canvas, col, row):
    """Create grid"""

    img = Image.open(name_canvas)
    width, height = img.size
    block_width = width // col
    block_height = height // row
    draw_sector = ImageDraw.Draw(img)

    for x in range(0, width, block_width):
        for y in range(0, height, block_height):
            draw_sector.rectangle((x, y, x + block_width, y +block_height), outline="orange")

    img.save("sector_300x300.jpg", "JPEG", quality=100)
    # сохранение картинки с секторами


def main():
    circle("blank_canvas.jpg")

if __name__ == '__main__':
    main()
