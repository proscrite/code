import cv2
import time
import os
import matplotlib
import numpy as np
import pandas as pd
from Constants import *
from matplotlib import pyplot as plt
from ast import literal_eval
import Camera
import Wheel
import Meter2    # Meter2 for TLPMX (new API version), Meter for TLMP (older version)
import saving
#matplotlib.interactive(True)

camera = Camera.Camera()
wheel = Wheel.Wheel()
meter = Meter.Meter()
data_struct = np.dtype([('date', 'double'), ('power', 'double'), ('name', str), ('images', (np.uint16, (24, 2048, 2048)))])


def time_date():
    return time.strftime(TIME_FORMAT)


def tif_file_name(filter_num, use_time=False):
    if use_time:
        return str(filter_num) + "_" + FILTERS[filter_num] + "_" + time_date() + ".tif"
    return str(filter_num) + "_" + FILTERS[filter_num] + ".tif"

def get_yes_no(question):
    while True:
        key = input(question)
        if key == 'y':
            return True
        elif key == 'n':
            return False
        else:
            print('invalid key')

def get_sample_name():
    while True:
        print_dict(SAMPLES)
        key = input('choose sample:\n')
        if (key.isnumeric()) and (int(key) == 0):
            return input('Write sample name\n')
        elif (key.isnumeric()) and (int(key) in SAMPLES):
            return SAMPLES[int(key)]
        else:
            print('invalid key')


def get_yes_no(question):
    while True:
        key = input(question)
        if key == 'y':
            return True
        elif key == 'n':
            return False
        else:
            print('invalid key')


def get_filters_to_snap():
    while True:
        print_dict(FILTERS)
        print('0:\tAll filters')
        key = input('choose filter to snap:\n')
        if (key.isnumeric()) and (int(key) == 0):
            return 0
        elif (key.isnumeric()) and (int(key) in FILTERS):
            return int(key)
        else:
            print('invalid key')

def get_nframes():
    while True:
        key = input('choose number of frames (default 400):\n')
        if (key.isnumeric()) and (int(key) == 0):
            return 400
        elif (key.isnumeric()):
            return int(key)
        else:
            print('invalid key')

def get_expTime():
    while True:
        key = input('Choose exposure time (default 0.5):\n')
        if (key.isnumeric()) and (int(key) == 0):
            return 0.5
        elif (key.isnumeric()):
            return key
        elif type(literal_eval(key)) == float:
            return key
        else:
            print('invalid key')

def print_dict(dict):
    print()
    for i in dict:
        print(str(i) + ':\t' + dict[i])


def print_image_set(image_set):
    fig_12img, ax_12img = plt.subplots(3, 4)
    fig_12img.tight_layout()
    cut = 500

    for row in range(3):
        for col in range(4):
            area = image_set[col + row * 4, cut:2048 - cut, cut:2048 - cut]
            img = ax_12img[row, col].imshow(area)
            title = str(FILTERS_BANDS[col + row * 4 + 1][0]) + '[nm], ' + str(FILTERS_BANDS[col + row * 4 + 1][1]) + '[nm]'
            ax_12img[row, col].set_title(title)
            ax_12img[row, col].axis('off')
            fig_12img.colorbar(img, ax=ax_12img[row, col])
    plt.show()  # block=False



def close_all_devices():
    camera.close()
    wheel.close()
    meter.close()


def imaging_manu():
    # name = ''
    # filters = None
    dark_image = True
    while True:
        name = get_sample_name()
        filters = get_filters_to_snap()
        if filters == 0:
            dark_image = get_yes_no('Take a dark images at the end? y/n\n')
        while True:
            if filters == 0:
                question = 'Sample:\t' + name + '\nAll filters\nDark image:\t' + str(dark_image)
            else:
                question = 'Sample:\t' + name + '\nFilter:\t' + FILTERS[filters]
            question += '\nTake image with this parameters? y/n\n'
            if get_yes_no(question):
                if open_all_devices() is False:
                    return
                take_images(name, filters, dark_image)
                close_all_devices()
            else:
                break
        if get_yes_no('Set new parameters? y/n\n') is False:
            break


def show_prop_camera():
    if camera.open() is False:
        return
    camera.show_prop_camera()
    camera.close()


def test():
    #wheel.open()
    print(meter.read())
    #if meter.open():
        #time.sleep(10)
     #   t = time.time()
      #  print(bool(meter))
        #print(meter.read())
       # print(time.time() - t)
    meter.close()


def leave(code=0):
    close_all_devices()
    exit(code)


def print_main_manu():
    print()
    for i in manu_def:
        print(i + ':\t' + manu_def[i])


manu = \
    {
        'i': imaging_manu,
        'a': test,
        'h': print_main_manu,
        'p': mean_power,
        'camera': show_prop_camera,
        'q': leave
    }

manu_def = \
    {
        'i': 'Taking images',
        'a': 'A test function',
        'p': 'Get power reading',
        'camera': 'Show the property of the camera',
        'h': 'List of commands',
        'q': 'quitting the program'
    }


def main():
    print_main_manu()
    while True:
        key = input('\nEnter a new command\nenter \'h\' for help\n')
        if key in manu:
            manu[key]()
        else:
            print("invalid key")


if __name__ == '__main__':
    main()


