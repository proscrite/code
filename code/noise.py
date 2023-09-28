# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 17:07:41 2022

@author: John
"""
import dcam
import os
import numpy as np
from matplotlib import pyplot as plt
# %matplotlib qt5 needs to add to code
from scipy.optimize import curve_fit
import scipy

TIME_OUT = 1000


def open_camera(iDevice=0): # connecting to the camera
    if dcam.Dcamapi.init() is not False:
        camera = dcam.Dcam(iDevice)
        if camera.dev_open() is not False:
            if camera.buf_alloc(1) is not False:
                camera.prop_setvalue(0x00470010, 1.0)   # DEFECT CORRECT MODE 1 = off, 2 = on
                camera.prop_setvalue(0x001F0130, 2.0)   # EXPOSURE TIME CONTROL 2 = normal
                return camera
            else:
                print('-NG: Dcam.buf_alloc(1) fails with error {}'.format(camera.lasterr()))
            camera.dev_close()
        else:
            print('-NG: Dcam.dev_open() fails with error {}'.format(camera.lasterr()))
    else:
        print('-NG: Dcamapi.init() fails with error {}'.format(dcam.Dcamapi.lasterr()))
    return False


def close_camera(camera): # closeing the camera
    camera.buf_release()
    camera.dev_close()
    dcam.Dcamapi.uninit()
    camera = False


def take_picture(camera): # get a numpy array of a picture from the camera (must be open)
    if camera.cap_snapshot() is not False:
        if camera.wait_capevent_frameready(TIME_OUT) is not False:
            data = camera.buf_getlastframedata()
            return data
    print("Failed taking a snapshot")
    camera_error = camera.lasterr()
    print('-NG: camera.wait_event() fails with error {}'.format(camera_error))


def poisson(k, lamda):
    #return np.multiply(np.power(lamda, k),np.divide(np.exp(-lamda),np.math.factorial(k)))
    return np.multiply(np.power(lamda, k),np.divide(np.exp(-lamda),scipy.special.factorial(k)))

def erlang(x, k, lamda):
    return np.multiply(np.power(lamda, k),np.power(x, k-1) ,np.divide(np.exp(-lamda*x),scipy.special.factorial(k-1)))


#%%
camera = open_camera()
if camera is False:
    print("error connecting to camera")
    
#%%
"""
histogram of pixel noise from 1 picture
should be taken with the camera covered for Dark Image
"""
if camera is not False: 
    camera.prop_setvalue(2031888, 0.2)  # EXPOSURE TIME
    data = take_picture(camera)
    data2 = np.concatenate(data)
    print("mean\t" + str(np.mean(data2)))
    print("median\t" + str(np.median(data2)))
    print("std\t" + str(np.std(data2)))
    fig = plt.figure(1)
    ax = plt.axes()
    ax.hist(data2, bins=np.arange(70,  150), density=True, alpha=0.75, rwidth=1)
    ax.grid(True)
#%%
"""
create a 3D array of 1000 pictures and saves it for ferther use
should be taken with the camera covered for Dark Image
"""

if camera is not False:
    pics_num = 1000
    data_set = np.zeros((pics_num, 2048, 2048), dtype=np.uint16)
    for i in range(pics_num):
        data_set[i]= take_picture(camera)
    np.save("set3", data_set)



#%%
if camera is not False:
    close_camera(camera)
#%%
"""
calculete the offset map of the camera for every pixel 
done from the data set of 1000 images
"""

offset = np.sum(data_set, axis=0)/pics_num
np.save("offset",offset)

#%%
"""
calculete the variance map of the camera for every pixel 
done from the data set of 1000 images
!!! might need restart to run as it takes a lot of RAM!!!
if you do reset load the data set and do not retake images
"""
var = np.sum((data_set - offset)**2, axis=0)/(pics_num-1)
np.save("var",var)
#%%
"""
reload the data_set
calculete the STD map of the camera for every pixel 
done from the data set of 1000 images
"""

data = np.load("set2.npy")
std = np.std(data,axis=0)
np.save("std",std)

#%%
"""
show the variance map
"""
var = np.load("var.npy")
ind_var = np.unravel_index(np.argmax(var), var.shape)
#var[var>400.0] = 400 # if you wish to cut large values for better visabilty
fig, ax = plt.subplots()
ax.imshow(var,cmap='gray',norm='linear',vmin=2,vmax=40)
ax.set_title("variance map")
#%%
"""
show the STD map
"""
std = np.load("std.npy")
ind = np.unravel_index(np.argmax(std), std.shape)
#std[std>60] = 60 # if you wish to cut large values for better visabilty
fig, ax = plt.subplots()
pic = ax.imshow(std,cmap='gray',norm='log', interpolation='none',vmin=1,vmax=5)
fig.colorbar(pic, ax=ax)
ax.set_title("STD map")
plt.ylabel('pixels')
plt.xlabel('pixels')


#%%
"""
show the offset map
"""
offset = np.load("offset.npy")
ind_offset = np.unravel_index(np.argmax(offset), offset.shape)
#offset[offset>200.0] = 200 # if you wish to cut large values for better visabilty
fig, ax = plt.subplots()
off = ax.imshow(offset,cmap='gray',norm='linear',vmin=97,vmax=120)
fig.colorbar(off, ax=ax)
ax.set_title("offset map")
plt.ylabel('pixels')
plt.xlabel('pixels')

#%%
"""
show hitogram of the STD map
"""
data = np.concatenate(std)
data = data[data<=5] # if you wish to cut large values for better visabilty
ax = plt.axes()
hist = ax.hist(data, bins=np.linspace(1.6,  5, 100), density=True, alpha=0.75, rwidth=1)
std_mean = np.mean(data)
std_std = np.std(data)
ax.set_title("normelized histogram of STD")
ax.annotate("std: " + str(std_std), (std_mean, 2))
ax.annotate("mean: " + str(std_mean), (std_mean, 1.75))
ax.axvline(x=np.mean(data),color='g',label='mean')

"""
an attempt to fit the histogram to a distribution
"""

#opt, cov = curve_fit(poisson, hist[1][:99], hist[0])
#cov = np.sqrt(np.diag(cov))
#pois = poisson(hist[1][:99], 1)
#ax.plot(hist[1][:99], pois)
#opt, cov = curve_fit(erlang, hist[1][:99], hist[0])
#cov = np.sqrt(np.diag(cov))
#erl = erlang(hist[1][:99], opt[0], opt[1])
#ax.plot(hist[1][:99], erl)
#%%
"""
show hitogram of the offset map
"""
data = np.concatenate(offset)
#data = data[data<=20] # if you wish to cut large values for better visabilty
ax = plt.axes()
hist = ax.hist(data, bins=np.linspace(105,  120, 100), density=True, alpha=0.75, rwidth=1)
offset_mean = np.mean(data)
offset_std = np.std(data)
ax.set_title("normelized histogram of offset")
ax.annotate("std: " + str(offset_std), (std_mean, 0.33))
ax.annotate("mean: " + str(offset_mean), (std_mean, 0.3))
ax.axvline(x=np.mean(data),color='g',label='mean')
#%%
offset = np.load("offset.npy")
data = np.concatenate(offset)
data = data[data>180]
ind_bad = []
bad_size = 0
M = np.argmax(offset)
bad_val = []
while M > 15000:
    bad_val.append(M)
    ind_bad.append(np.unravel_index(M, offset.shape))
    offset[ind_bad[bad_size][0]][ind_bad[bad_size][1]] = 0
    M = np.argmax(offset)
    bad_size += 1








