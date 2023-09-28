import time
import os
import numpy as np
from Constants import *
#import cv2
from PIL import Image
import piexif
import subprocess
import re


def read_exif(filename):
    result = subprocess.run([EXIFTOOL_APP, filename], stdout=subprocess.PIPE)
    _res = result.stdout.decode("utf-8").split("\n")
    res = {}
    for p in _res:
        field = re.split(" +: ", p)
        if len(field) == 2:
            res[field[0]] = field[1]
    return res


def set_exif_field(filename, field, value):
    result = subprocess.run([EXIFTOOL_APP, '-' + str(field) + '="' + str(value) + '" ', filename], stdout=subprocess.PIPE)

    if re.search(EXIFTOOL_OK_STRING, result.stdout.decode('utf-8')):
        return True
    return False


def save_npy(data, name):
    today = time.strftime(TIME_FORMAT_TODAY)
    path = NP_SAVE_LOCATION + today

    if not os.path.exists(path):
        os.makedirs(path)

    path += '\\' + name

    if not os.path.exists(path):
        os.makedirs(path)

    files = os.listdir(path)

    num = -1
    for file in files:
        if file.endswith('.npy'):
            num = max(num, int(file[:-4]))

    num += 1
    file_name = f"{num}.npy"
    path += '\\' + file_name
    np.save(path, data)
    return num


def single_tif_save(data, name, power, filters):
    today = time.strftime(TIME_FORMAT_TODAY)
    path = IMAGE_SINGLE_SAVE_LOCATION + today

    if not os.path.exists(path):
        os.makedirs(path)

    path += '\\' + name

    if not os.path.exists(path):
        os.makedirs(path)

    path += '\\' + FILTERS[filters] + time.strftime('_%H-%M-%S') + '.tif'

    imax = np.amax(data)
    if imax > 0:
        image_multiplayer = int(65535 / imax)
        data = data * image_multiplayer
    else:
        image_multiplayer = 1

    img = Image.fromarray(data)
    img.save(path)

    # set_exif_field(path, 'ExposureTime', int(FILTERS_EXPOSER[filters]*1000))) # problem writing into
    set_exif_field(path, 'ImageDescription', name)
    set_exif_field(path, 'DateTimeOriginal', time.localtime())
    set_exif_field(path, 'Artist', AURTHUR)
    comment = 'Laser power:' + str(power) + ',Value stretch factor:' + str(image_multiplayer) \
        + ',Exposure Time:' + str(int(FILTERS_EXPOSER[filters]*1000))
    set_exif_field(path, 'XPComment', comment)


def save_tif_set(data, name, power, num):
    today = time.strftime(TIME_FORMAT_TODAY)
    path = IMAGE_SET_SAVE_LOCATION + today

    if not os.path.exists(path):
        os.makedirs(path)

    path += '\\' + name

    if not os.path.exists(path):
        os.makedirs(path)

    path += '\\' + str(num)

    if not os.path.exists(path):
        os.makedirs(path)
    t = time.strftime('_%H-%M-%S')
    for filters in range(NUMBER_OF_FILTERS):
        path_file = path + '\\' + str(FILTERS[filters+1]) + t + '.tif'

        imax = np.amax(data[filters])
        if imax > 0:
            image_multiplayer = int(65535 / imax)
            data = data * image_multiplayer
        else:
            image_multiplayer = 1

        img = Image.fromarray(data[filters])
        img.save(path_file)

        # set_exif_field(path, 'ExposureTime', int(FILTERS_EXPOSER[filters]*1000))) # problem writing into
        set_exif_field(path_file, 'ImageDescription', name)
        set_exif_field(path_file, 'DateTimeOriginal', time.localtime())
        set_exif_field(path_file, 'Artist', AURTHUR)
        comment = 'Laser power:' + str(power) + ',Value stretch factor:' + str(image_multiplayer) \
            + ',Exposure Time:' + str(int(FILTERS_EXPOSER[filters+1]*1000))
        set_exif_field(path, 'XPComment', comment)


def save_tiff(data, num, name, power, filters=1):
    print('Saving .tif files.')
    if num == -1:
        single_tif_save(data, name, power, filters)
    else:
        save_tif_set(data, name, power, num)


if __name__ == '__main__':
    a = np.random.random((12, 10, 10))
    save_tiff(a, 1, 'test_sample', 0.000123, 7)
    """
    for i in range(10):
        data = np.random.random((10, 10))
        save_npy(data, 'test1')

    for i in range(10):
        data = np.random.random((10, 10))
        save_npy(data, 'test2')
    """












