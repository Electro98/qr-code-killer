from PIL import Image
import cv2


def add_to_img_(image):
    """
    'сюда изображение с значком подай'
    добавляет на картинку ваш закодированный код
    """
    znak = Image.open('znak.jpg')  # это моя оболочка ее нужно оставить
    znak_orginal = image  # сюда подается ваше изображение

    znak.paste(znak_orginal, (0, 0))

    # znak.save("ready1.jpg")  # это изображение с каритнкой
    return znak


def cut_image(image_path):
    """

    вырезает с картинки кружок с нашим кодом
    :return:
    """

    image = cv2.imread(image_path) # изображение где ищем
    im = Image.open(image_path)  # изображение где ищем
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(gray, 10, 250)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.05 * peri, True)
        if len(approx) != 4:
            continue
        rect = cv2.boundingRect(c)
        width, height = rect[2:]
        if height != 90 and width != 395:
            continue
        rect1 = rect
        a = rect1[0]
        b = rect1[1]
    crok = im.crop((a - 204, b - 640, a + rect1[2], b - 40))
    return crok
