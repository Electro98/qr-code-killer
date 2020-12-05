
import math

from bitstring import BitArray
from PIL import Image, ImageDraw


def coordinator_(radius, offset_cenx=0, offset_ceny=0, *, num=360, offset_angle=0.008726, **kwargs):
    '''Фабрика для функции считающей координаты'''
    angle = math.pi*2/num

    def coordinate(index) -> (int, int):
        x = math.cos(angle*index+offset_angle)*radius + offset_cenx
        y = math.sin(angle*index+offset_angle)*radius + offset_ceny
        return x, y

    return coordinate


def get_bits_from_image(image: Image.Image, radius_1, radius_2, **kwargs) -> BitArray:
    '''Эта функция считывает все кодированные биты с кольца на изображении

    :param method:
        :image: изображение, с которого нужно прочитать биты
        :radius_1: радиус первого закодированного кольца
        :radius_2: радиус второго закодированного кольца
        :**kwargs: доп. аргументы смотрите на аргументы coordinator

    :returns BitArray'''

    num = 360 if not kwargs['num'] else kwargs['num']
    offset = image.width // 2, image.height // 2

    coordinate_1 = coordinator_(radius_1, *offset, **kwargs)
    coordinate_2 = coordinator_(radius_2, *offset, **kwargs)

    array_of_bit = BitArray(num * 2)

    for i in range(num):
        array_of_bit[i] = 1 if sum(pix[coordinate_1(i)]) < 50 else 0
        array_of_bit[i + num] = 1 if sum(pix[coordinate_1(i)]) < 50 else 0

    return array_of_bit


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
