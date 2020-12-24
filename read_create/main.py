
import math

from bitstring import BitArray
from PIL import Image, ImageDraw


def coordinator_(radius, offset_cenx=0, offset_ceny=0, *, num=120, offset_angle=0.026179, **kwargs):
    '''Фабрика для функции считающей координаты'''
    angle = math.pi*2 / num

    def coordinate(index) -> (int, int):
        x = math.cos(angle*index + offset_angle)*radius + offset_cenx
        y = math.sin(angle*index + offset_angle)*radius + offset_ceny
        return x, y

    return coordinate


def get_bits_from_image_(image: Image.Image, radiuses: list, **kwargs) -> BitArray:
    '''Эта функция считывает все кодированные биты с кольца на изображении

    :param method:
        :image: изображение, с которого нужно прочитать биты
        :radiuses: радиусы закодированных колец
        :**kwargs: доп. аргументы смотрите на аргументы coordinator

    :returns BitArray'''

    num = 120 if not kwargs.get('num') else kwargs['num']
    offset = image.width // 2, image.height // 2
    pix = image.load()

    coordinates = [coordinator_(radius, *offset, **kwargs) for radius in radiuses]
    num_of_raduises = len(radiuses)

    array_of_bit = BitArray(num * num_of_raduises)

    for i in range(num):
        for j in range(num_of_raduises):
            array_of_bit[i + j * num] = 1 if sum(pix[coordinates[j](i)]) < 120 else 0

    return array_of_bit


def encode_str_(text: str, size = 360) -> BitArray:
    '''Эта функция кодирует текст в массив битов

    :param method:
        :text: кодируемый текст, по умолчание не длиньше 44 символов
        :size: необходимый размер массива битов

    :returns BitArray

    Примечание: длина текста считается так size//8 - 1'''
    # Избавляемся от лишнего текста и кодируем
    text = text[:size//8 - 1]
    encoded_text = text.encode('windows-1251', 'replace')

    result_bit_array = BitArray(size)
    result_bit_array.overwrite(encoded_text, 8)

    return result_bit_array

def decode_str_(encoded_text: BitArray) -> str:
    '''Эта функция декодирует текст из массива битов

    :param method:
        :encoded_text: закодированный текст, с системной информацией

    :returns str:'''
    # Отрезаем системную информацию
    encoded_text = encoded_text[8:]
    decoded_text = encoded_text.bytes.decode('windows-1251', 'replace')

    return decoded_text


def create_coded_rings_(information: BitArray, img) -> Image.Image:
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
                
    elif 120 < len(information) < 241:
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

    elif 240 < len(information) < 361:
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

        for i in range(len(information)):
            if not i % 3:
                j = i // 3
                if j < len(third):
                    if third[j]:
                        sectors.arc((23, 23, width - 23, height - 23), i, i + 3, fill = "black", width = 10)
                    else:
                        sectors.arc((23, 23, width - 23, height - 23), i, i + 3, fill = "white", width = 10)

    # img.save("coded_rings.jpg", "JPEG", quality=100)
    return img


def unite_images_(image: Image.Image, rings: Image.Image) -> Image.Image:
    """Функция объединения всех частей
    :param image: Изображение с логотипом
    :param ring: Изображение с кольцами
    """
    
    # Изображение с лого
    img_logo = image
    width, height = img_logo.size
    x = (width - height)//2
    img_cropped = img_logo.crop((x, 0, x+height, height))
    mask = Image.new("L", img_cropped.size)

    mask_draw = ImageDraw.Draw(mask)
    width, height = img_cropped.size
    mask_draw.ellipse((36, 36, width - 36, height - 36), fill=255)
    img_cropped.putalpha(mask) 

    img_ring = rings
    obj = img_cropped.load()

    for x in range(width):
        for y in range(height):
            if obj[x, y][3] != 0:
                img_ring.putpixel((x,y), (obj[x, y][0], obj[x, y][1], obj[x, y][2]))

    # img_ring.save("QRcode_killer.jpg", "JPEG", quality=100)
    return img_ring


def create_encoded_image(image: Image.Image, text: str) -> Image.Image:
    '''Эта функция создаёт изображение с закодированным текстом

    :param method:
        :image: лого, которое окажется по середине
        :text: текст, который окажется закодирован

    :returns Image'''
    resized_image = image.resize((600, 600), Image.LANCZOS)

    encoded_bits = encode_str_(text)
    rings_image = create_coded_rings_(encoded_bits, Image.open('circles.jpg'))
    united_image = unite_images_(resized_image, rings_image)
    return united_image


def get_text_from_image(image: Image.Image, radiuses=(292, 282, 272)) -> str:
    '''Эта функция получает текст из изображения с закодированным текстом

    :param method:
        :image: изображение с закодированным текстом
        :radiuses: радиусы колец с информацией

    :returns str'''
    encoded_bits = get_bits_from_image_(image, radiuses)
    return decode_str_(encoded_bits)


def main():
    #encoded_bits = encode_str_('Hello, мазафака. It\'s alive!')
    #rings = create_coded_rings_(encoded_bits, Image.open('circles.jpg'))
    #unite_images_(Image.open('2.jpg'), rings)
    create_encoded_image(Image.open('1.jpg'), 'Hello, мазафака. It\'s alive!')
    print(get_text_from_image(Image.open('QRcode_killer.jpg')))


if __name__ == '__main__':
    main()
