from .get_filename_by_id import get_filename_by_id
from PIL import Image
from .constants import *
import os


def save_image(filename, id):
    """ Скопировать и сконвертировать изображение """
    # Создать папку если не существует
    if not os.path.exists(ROOT + 'images'):
        os.mkdir(ROOT + 'images')
    im = Image.open(filename)
    im2 = None
    # Задать новый размер изображению
    x, y = im.size
    nx, ny = 700, 450
    nratio = nx / ny
    ratio = x / y
    if ratio > nratio:
        xratio = nx / x
        height = int(xratio * y)
        im2 = im.resize((nx, height))
    elif ratio < nratio:
        yratio = ny / y
        width = int(yratio * x)
        im2 = im.resize((width, ny))
    # Скопировать изображения с изменениями
    copy_filename = get_filename_by_id(id)
    im2.save(copy_filename)
