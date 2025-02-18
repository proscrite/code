import cv2
import time
import os
import numpy as np
import pandas as pd
from Constants import *
from matplotlib import pyplot as plt
from ast import literal_eval
import Camera
import Wheel
import Meter2    # Meter2 for TLPMX (new API version), Meter for TLMP (older version)
import saving
import SetupSettings
#matplotlib.interactive(True)

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
        elif (key == 'q'):
            return 'exit'
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

global texp

class Setup:
    def __init__(self):
        self.camera = Camera.Camera()
        self.wheel = Wheel.Wheel()
        self.meter = Meter2.Meter()
        self.settings = pd.DataFrame()
        
        self.menu = \
            {
            'i': (self.take_spectra, 'Taking images'),
            'f': (self.image_filter, 'Take single filter'),
            'a': (self.test, 'A test function'),
            'h': (0, 'List of commands'),
            'p': (self.mean_power, 'Get power reading'),
            'camera': (self.show_prop_camera, 'Show camera proerties'),
            's': (self.set_cam_properties, 'Set camera property'),
            'e': (self.set_exposure, 'Set camera exposure'),
            't': (self.time_evolution, 'Take time evolution'),
            's': (self.take_sequence, 'Take sequence'),
            ',': (self.settings_menu, 'Settings menu'),
            'q': (self.leave, 'quit')
        }


    def __del__(self):
        if self:
            self.close_all_devices()

    def print_menu(self, mode):
        if mode == 'main': menu = self.menu
        elif mode == 'set': menu = self.menu_settings
        print()
        for i in menu.keys():
            print(i + ':\t' + menu[i][1])

    def take_single_frame(self, name, path, filters):
        self.wheel.set_filter(filters)
        self.camera.exposure_time(self.camera.exposure)
        print('Camera exposure in single frame: ', self.camera.exposure)
        data = self.camera.take_picture()
        power = self.meter.read()
        # num = saving.save_npy(data, name)
        saving.single_tif_save(data, path, name, power, filters)

    def take_images(self, name, filters):
        if filters != 0:
            rootpath = IMAGE_SINGLE_SAVE_LOCATION
            path = saving.check_path_save(rootpath, name)
            self.take_single_frame(name, path, filters)
            power = self.meter.read()
            print('Power after self.take_single_frame(): ', power)
            self.settings = SetupSettings.add_settings_value(self.settings, 'Power(W)', power)
            SetupSettings.write_settings(path, self.settings)

        else:
            data_set = np.zeros(1, dtype=data_struct)
            data_set['date'][0] = np.double(time.time())
            data_set['name'][0] = name
            rootpath = IMAGE_SET_SAVE_LOCATION
            print('Before loop: current exposure is %0.2f s \n' %(self.camera.exposure) )

            for i in range(11, -1, -1):
                self.wheel.set_filter(i+1)
                print("Current filter: %i" %(i+1))
                self.camera.exposure_time(self.camera.exposure)
                print('Current exposure is %0.2f s \n' %(self.camera.exposure) )
                
            #    camera.exposure_time(FILTERS_EXPOSER[i + 1])
                data_set['images'][0][i] = self.camera.take_picture()
            data_set['power'][0] = self.meter.read()

            save_path = saving.save_tif_set(data_set['images'][0], name, data_set['power'][0])
            power = self.meter.read()
            self.settings = SetupSettings.add_settings_value(self.settings, 'Power(W)', power)

            SetupSettings.write_settings(save_path, self.settings)
            print_image_set(data_set['images'][0])
            print()

    def mean_power(self):
        if self.meter.open(1):
            print(f'Power: {self.meter.read()} W')
            time.sleep(1)
        self.meter.close()

    def open_all_devices(self):
        while True:
            if not(self.camera.open() and self.wheel.open()):
                if get_yes_no('Try again? y/n\n') is False:
                    return False
            else:
                break
        self.meter.open()
        return True

    def close_all_devices(self):
        self.camera.close()
        self.wheel.close()
        self.meter.close()

    def take_spectra(self):
        while True:
            name = get_sample_name()
            filters = 0
        
            question = 'Sample:\t' + name + '\nAll filters\n' 
            question += '\nTake image with this parameters? y/n\n'
            if get_yes_no(question):
                if self.open_all_devices() is False:
                    return
                self.take_images(name, filters)
                self.close_all_devices()
            else:
                break

    def image_filter(self):
        while True:
            name = get_sample_name()
            if name == 'exit': break
            filters = get_filters_to_snap()
            #if filters == 0:
                #dark_image = get_yes_no('Take a dark images at the end? y/n\n')
            if filters == 0:
                question = 'Sample:\t' + name + '\nAll filters\n' #Dark image:\t' + str(dark_image)
            else:
                question = 'Sample:\t' + name + '\nFilter:\t' + FILTERS[filters]
            #question += 'Current exposure is %0.2f s, do you want to change it? (y/n) \n' %(camera.exposure)
            question += '\nTake image with this parameters? y/n\n'
            while get_yes_no(question):
                if self.open_all_devices() is False:
                    return
                self.take_images(name, filters)
                self.close_all_devices()
            else:
                break
            
    def time_evolution(self):
        name = get_sample_name()
        while True:
            filters = get_filters_to_snap()
            if filters != 0:
                break
        nframes = get_nframes()
        question = 'Sample:\t' + name + '\nFilter:\t' + FILTERS[filters] 
        question += '\nNumber of frames:\t %i \n' %nframes
        question += '\nTake image with this parameters? y/n\n'
        if get_yes_no(question):
            if self.open_all_devices() is False:
                return
            rootpath = IMAGE_TIMERUN_SAVE_LOCATION
            path = saving.check_path_save(rootpath, name)
            for i in range(nframes):
                print("Frame nr. %i" %i)
                self.take_single_frame(name, path, filters)
            SetupSettings.write_settings(path, self.settings)
            self.close_all_devices()
            
    def take_sequence(self):
        if self.open_all_devices() is False:
                return
        print('Devices open, taking sequence')
        data = self.camera.take_sequence()
        print(data)

    def set_exposure(self):
        if self.camera.open() is False:
            return
        question = 'Current exposure is %0.2f s, do you want to change it? (y/n) \n' %(self.camera.exposure)
        if get_yes_no(question):
            texp = float(get_expTime())
            self.camera.exposure_time(texp)
            self.settings = SetupSettings.add_settings_value(self.settings, 'EXPOSURE_TIME', texp)
        self.camera.close()

    def show_prop_camera(self):
        if self.camera.open() is False:
            return
        self.camera.show_prop_camera()
        self.camera.close()

    def set_cam_properties(self):
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

    def leave(self, code=0):
        self.close_all_devices()
        exit(code)

    def init_settings(self):
        fin = SetupSettings.find_recent_settings()
        print('Loading recent settings at :', fin)
        self.settings = SetupSettings.read_settings(fin)

    def settings_menu(self):
        self.settings = SetupSettings.edit_settings(self.settings)


def main():
    st = Setup()
    st.init_settings()
    # st.camera.open()
    # st.camera.exposure_time(EXPOSURE_TIME)
    while True:
        st.print_menu('main')
        key = input('\nEnter a new command\nenter \'h\' for help\n')
        if key == 'h':
            pass
        elif key in st.menu:
            st.menu[key][0]()
        else:
            print("invalid key")


if __name__ == '__main__':
    main()


