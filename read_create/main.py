
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
    """Функция для перевода текста в массив из бит
    :param text: исходный текст
    :returns bit_text
    """
    # Функция сделана не полностью, потому что у каждого символа
    # (заглавной и прописной буквы) разная длина
    # для записи это не имеет значения, но для чтения нужно сделать нормально
    
    bit_text = []
    for symbol in text:
    # перевод всех символов в числовое значение

        symbol = ord(symbol)

        while symbol > 0:
        # цикл для перевода в двоичную сс

            symbol_bit = str(symbol % 2)
            symbol = symbol // 2
            bit_text.append(symbol_bit)

    return bit_text


def create_coded_rings_(information: BitArray) -> Image.Image:
    """Функция для создания закодированного кольца
    :param information: биты закодированного текста
    :param img: экземпляр класса Image
    :returns Image.Image
    """
    width, height = img.size
    sectors = ImageDraw.Draw(img)

    if len(information) < 121:
    # кодирование 1 круга
        for i in range(360):
            if not i % 3:
                j = i // 3
                if j < len(information):
                if information[j]:
                    sectors.arc((3, 3, width - 3, height - 3), i, i + 3, fill = "black", width = 10)
                else:
                    sectors.arc((3, 3, width - 3, height - 3), i, i + 3, fill = "white", width = 10)
                
    elif 120 < len(q) < 241:
    # кодирование 2 кругов

        second = information[120:len(information)+1]
        
        for i in range(360):
            if not i % 3:
                j = i // 3
                if information[j]:
                    sectors.arc((3, 3, width - 3, height - 3), i, i + 3, fill = "black", width = 10)
                else:
                    sectors.arc((3, 3, width - 3, height - 3), i, i + 3, fill = "white", width = 10)

        for i in range(360):
            if not i % 3:
                j = i // 3
                if j < len(second):
                    if second[j]:
                        sectors.arc((13, 13, width - 13, height - 13), i, i + 3, fill = "black", width = 10)
                    else:
                        sectors.arc((13, 13, width - 13, height - 13), i, i + 3, fill = "white", width = 10)

    elif 240 < len(q) < 361:
    # кодирование 3 кругов

        second = information[120:241]
        third = information[240:len(information)+1]

        for i in range(360):
            if not i % 3:
                j = i // 3
                if information[j]:
                    sectors.arc((3, 3, width - 3, height - 3), i, i + 3, fill = "black", width = 10)
                else:
                    sectors.arc((3, 3, width - 3, height - 3), i, i + 3, fill = "white", width = 10)

        for i in range(360):
            if not i % 3:
                j = i // 3
                if second[j]:
                    sectors.arc((13, 13, width - 13, height - 13), i, i + 3, fill = "black", width = 10)
                else:
                    sectors.arc((13, 13, width - 13, height - 13), i, i + 3, fill = "white", width = 10)

        for i in range(len(q)):
            if not i % 3:
                j = i // 3
                if j < len(third):
                    if third[j]:
                        sectors.arc((23, 23, width - 23, height - 23), i, i + 3, fill = "black", width = 10)
                    else:
                        sectors.arc((23, 23, width - 23, height - 23), i, i + 3, fill = "white", width = 10)

    return # не знаю что должен возращать


def unite_images_(image: Image.Image, rings: Image.Image) -> Image.Image:
    pass


def main():
    pass


if __name__ == '__main__':
    main()
