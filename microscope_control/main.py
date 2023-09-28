import cv2
import time
import os
import matplotlib
import numpy as np
from Constants import *
from matplotlib import pyplot as plt
import Camera
import Wheel
import Meter
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


def mean_power():
    if meter.open(3):
        print(meter.read())
    meter.close()


# def save_image(data, name, power):
#     if data.dtype == np.uint16:
#         imax = np.amax(data)
#         if imax > 0:
#             imul = int(65535 / imax)
#             # print('Multiple %s' % imul)
#             data = data * imul
#             cv2.imwrite(name, data)  # check success?
#             return True
#     return False
#
#
# def create_data_set(filter_to_snap=0, test_power=True):
#     if camera.open() is False:
#         return False
#     if wheel.open() is False:
#         return False
#     start_time = time_date()
#     power = None
#     folder_name = IMAGE_SAVE_LOCATION + start_time
#     os.mkdir(folder_name)
#     directory = os.getcwd()
#     os.chdir(directory)
#     if filter_to_snap != 0:
#         wheel.set_filter(filter_to_snap)
#         camera.exposure_time(FILTERS_EXPOSER[filter_to_snap])
#         data = camera.take_picture()
#         name = folder_name + "\\" + tif_file_name(filter_to_snap, 1)
#         save_image(data, name)
#         return True
#     data_set = np.zeros((12, 2048, 2048), dtype=np.uint16)
#     for i in FILTERS:
#         wheel.set_filter(i)
#         camera.exposure_time(FILTERS_EXPOSER[i])
#         data_set[i - 1] = camera.take_picture()
#         name = folder_name + "\\" + tif_file_name(i, 1)
#         save_image(np.copy(data_set[i - 1]), name)
#
#     if test_power:
#         print('Measuring power: (may take a few seconds)')
#         power = mean_power()
#     if power is np.nan:
#         name = NP_SAVE_LOCATION + start_time
#     else:
#         name = NP_SAVE_LOCATION + start_time + F'_{mean_power():.5g}' + '[W]'
#     np.save(name, data_set)
#     print('numpy file name is:\t' + name + '.npy')
#     os.chdir(directory)
#     return


def take_images(name, filters, dark_img):
    if filters != 0:
        wheel.set_filter(filters)
        camera.exposure_time(FILTERS_EXPOSER[filters])
        data = camera.take_picture()
        power = meter.read()
        saving.save_tiff(data, -1, name, power, filters)
    else:
        data_set = np.zeros(1, dtype=data_struct)
        data_set['date'][0] = np.double(time.time())
        data_set['name'][0] = name
        for i in range(NUMBER_OF_FILTERS):
            wheel.set_filter(i+1)
            camera.exposure_time(FILTERS_EXPOSER[i + 1])
            data_set['images'][0][i] = camera.take_picture()
        data_set['power'][0] = meter.read()
        if dark_img:
            input('Taking dark images\nCover laser and then press enter\n')
            for i in range(NUMBER_OF_FILTERS):
                wheel.set_filter(i + 1)
                camera.exposure_time(FILTERS_EXPOSER[i + 1])
                data_set['images'][0][i+12] = camera.take_picture()
        num = saving.save_npy(data_set, name)
        print('File number is:\t' + str(num))
        saving.save_tiff(data_set['images'][0], num, name, data_set['power'][0])
        print_image_set(data_set['images'][0])
        print()


def print_dict(dict):
    print()
    for i in dict:
        print(str(i) + ':\t' + dict[i])


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


def open_all_devices():
    while True:
        if not(camera.open() and wheel.open()):
            if get_yes_no('Try again? y/n\n') is False:
                return False
        else:
            break
    meter.open()
    return True


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


