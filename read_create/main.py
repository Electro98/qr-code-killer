
import math

from bitstring import BitArray
from PIL import Image


def coordinator_(radius, offset_cenx=0, offset_ceny=0, *, num=120, offset_angle=0.026179, **kwargs):
    '''Фабрика для функции считающей координаты'''
    angle = math.pi*2 / num

    def coordinate(index) -> (int, int):
        x = math.cos(angle*index + offset_angle)*radius + offset_cenx
        y = math.sin(angle*index + offset_angle)*radius + offset_ceny
        return x, y

    return coordinate


def get_bits_from_image(image: Image.Image, radiuses: list, **kwargs) -> BitArray:
    '''Эта функция считывает все кодированные биты с кольца на изображении

    :param method:
        :image: изображение, с которого нужно прочитать биты
        :radiuses: радиусы закодированных колец
        :**kwargs: доп. аргументы смотрите на аргументы coordinator

    :returns BitArray'''

    num = 120 if not kwargs['num'] else kwargs['num']
    offset = image.width // 2, image.height // 2
    pix = image.load()

    coordinates = [coordinator_(radius, *offset, **kwargs) for radius in radiuses]

    array_of_bit = BitArray(num * 2)

    for i in range(num):
        for radius, j in enumerate(radiuses):
            array_of_bit[i + j * num] = 1 if sum(pix[coordinates[j](i)]) < 50 else 0

    return array_of_bit


def create_coded_image(image: Image.Image, text: str) -> Image.Image:
    pass


def code_str_(text: str) -> BitArray:
    pass


def create_coded_rings_(information: BitArray) -> Image.Image:
    pass


def unite_images_(image: Image.Image, rings: Image.Image) -> Image.Image:
    pass


def main():
    pass


if __name__ == '__main__':
    main()
