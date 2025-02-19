import sys
sys.path.append(r'C:\Users\owner\Documents\thorlabs_apt-master')

import cv2
import time
from PIL import Image

import os
import matplotlib
import numpy as np
import time
from Constants import *
from matplotlib import pyplot as plt
from scipy.stats import kurtosis

from ast import literal_eval
import Camera
from pylablib_DCAM.devices.DCAM import DCAMCamera
import Wheel
import Meter
import saving
#matplotlib.interactive(True)


import thorlabs_apt as apt
# apt.list_available_devices()
motor = apt.Motor(26002227)
# motor.move_home(True)

path0 = r"G:\My Drive\Ba Tagging\code\imag_analisis\focustest\focustests_Mitutoyo\10um_500steps"
name = 'test'
filters = 1
# camera = Camera.Camera()
camera = DCAMCamera(idx=0)
meter = Meter.Meter()


def set_exposure():
    if camera.open() is False:
        return
    question = 'Current exposure is %0.2f s, do you want to change it? (y/n) \n' %(camera.exposure)
    if get_yes_no(question):
        texp = float(get_expTime())
        camera.set_exposure(texp)

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

def get_yes_no(question):
    while True:
        key = input(question)
        if key == 'y':
            return True
        elif key == 'n':
            return False
        else:
            print('invalid key')

def move_mm():
    motor.move_by(1)

def move_100micron():
    motor.move_by(0.1)

def move_micron():
    motor.move_by(0.001)

def single_tif_save(data, path, pos):
    
    path += '\\' + str(pos) + '.tif'
    imax = np.amax(data)
    if imax > 0:
        image_multiplayer = int(65535 / imax)
        data = data * image_multiplayer
    else:
        image_multiplayer = 1

    img = Image.fromarray(data)
    img.save(path)

def loop_step(step, nstep, initPos, path0):
    kurt = []
    avgint = []
    positions = []

    pathd = path0# + str(step) + 'mm'
    try:
        os.makedirs(pathd)
    except FileExistsError: pass

    for i in range(nstep):
        # time.sleep(1)
        motor.move_by(step)
        print("Position:", initPos+step*(i+1))

        print("Pos motor:", motor.position)
        positions.append(motor.position)

        time.sleep(1)

        data = camera.snap(timeout=15)

        curPos = round( initPos+step*(i+1), 2) * 1e3
        path = pathd +'\\' + 'Im_pos' + str(curPos).zfill(3) + 'um.tif'
        img = Image.fromarray(data)
        img.save(path)

        dataim = data.astype(np.int64)
        k = kurtosis(dataim.flatten(), fisher=True, bias=False )
        avgim = np.average(dataim)
        kurt.append(k/avgim)
        
        avgint.append(avgim)

    fig = plt.figure()
    plt.plot(positions, kurt, 'o-', label='Kurtosis')
    plt.gca().set(xlabel = f'Step ({step} µm)', ylabel= 'Kurtosis / avg int. (arb. units)')
    fig.savefig(pathd+'/kurtosis.png')
    plt.show()

    fig2 = plt.figure()
    plt.plot(positions, avgint, 'ro-', label='Avg. intensity')
    plt.gca().set(xlabel = f'Step ({step} µm)', ylabel= 'Average int. (arb. units)')
    fig2.savefig(pathd+'/avg_int.png')
    plt.show()

    posmin = np.argmin(kurt)
    posmax = np.argmax(avgint) 
    return positions[posmin], positions[posmax]
    
def test_position(initPos, step):
    motor.move_by(step)
    should = round( initPos+step, 2) 
    actualPos = motor.position

    if abs(actualPos - should) > 0.015:
        print("Insufficient sleep time for init position, homing...")
        motor.move_home(True)
        time.sleep(45)
        exit

def dummy_autofocus(files, flag_plot=False):
    metric = []

    # img0 = self.camera.get_frame()    # For live autofocus
    img0 = io.imread(files[0]).astype(np.int16)
    _, best_area, best_region = find_fov(img0)
    circ_mask = offset_circular_mask(img0, best_region, best_area, flag_plot=flag_plot)

    # for n in nsteps:
        # motor.move(n)
        # img = self.camera.get_frame()
    for f in files:
        img = io.imread(f).astype(np.int16) 
        img[~circ_mask] = 0
        img = exposure.equalize_hist(img)
        metric.append(laplacian(img))

    if flag_plot:
        plt.plot(metric, 'o-')
        plt.legend()

    # return np.argmin(metric), metric
    return metric

def main(path0):
    print("Initialize camera")
    camera.open()
    power = meter.read()

    # set_exposure()
    camera.set_exposure(0.5)
    print("Exposure: ", camera.get_exposure())

    # motor.move_home()
    # time.sleep(45)
    # print('Finished homing')
    initPos = 21.0
    motor.move_to(initPos)
    print("Pos motor:", motor.position)
    input('Continue?')

    print('Moved to', initPos )
    step1 = 0.1
    nsteps1 = 500
    step2 = -0.01
    
    # test_position(initPos, step2)

    kurtmin, avgmax = loop_step(step2, nsteps1, initPos, path0)

    print('Min pos. is ', kurtmin)
    print('Max avg. is ', avgmax)

    # motor.move_to(initPos)
    # print('Moved to', initPos ) 
    # motor.move_by(step1*posmin)
    # print('Moved: ', step1*posmin)

    # data = camera.take_picture()
    # plt.imshow(data, clim=(100, 800))
    # plt.colorbar()
    # plt.show()
    
if __name__ == '__main__':
    main(path0)
