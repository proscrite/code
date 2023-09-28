# -*- coding: utf-8 -*-
"""
Created on Tue May 30 16:19:58 2023

@author: Nir Kapon
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.optimize import curve_fit
from scipy.interpolate import InterpolatedUnivariateSpline

# %matplotlib qt5

data_location = 'C:\\Users\\John\\My Drive\\Ba Tagging\\profile_laser_on_sample\\'
image0 = 'NONAME001.TIF'

QE_location = "C:\\Users\\John\\My Drive\\Ba Tagging\\code\\QE calc\\"
QE_DATA_FILE = QE_location+ "QE_data.csv"

pixel_length = 6.5e-6
electron_to_count = 0.46

def sort_array(x, y):
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]
    arrlinds = x.argsort()
    x = x[arrlinds[0::]]
    y = y[arrlinds[0::]]
    return x, y


def fined_loc(x, band): # band is of the shape (number, number)
    low = band[0]
    high = band[1]
    loc_low = -1
    loc_high = -1
    for i in range(len(x)):
        if loc_low == -1:
            if x[i] > low:
                loc_low = i - 1
        else:
            if x[i] > high:
                loc_high = i - 1
                break
    return loc_low, loc_high


def QE(band):   # band is of the shape (number, number)
    x = np.genfromtxt(QE_DATA_FILE, delimiter=',', usecols=(0))
    y = np.genfromtxt(QE_DATA_FILE, delimiter=',', usecols=(1))
    x, y = sort_array(x, y)
    f = InterpolatedUnivariateSpline(x, y, k=1)
    loc_low, loc_high = fined_loc(x, band)
    qe = f.integral(x[loc_low], x[loc_high])
    qe /= (x[loc_high] - x[loc_low])
    return qe
    


def gaussian(x, a, x0, sigma):
    return a * np.exp(-(x-x0)**2 / (2*sigma **2))    


def get_pic(name):
    pic = Image.open(name)#.convert('L')
    pic = np.asarray(pic)
    pic_fig, pic_ax = plt.subplots()
    img = pic_ax.imshow(pic)
    pic_ax.axis('off')
    pic_fig.colorbar(img, ax=pic_ax)
    pic_x = pic.sum(axis=0)
    pic_y = pic.sum(axis=1)
    return pic_x, pic_y

#%%

band_range = (390,410)
QE_in_band = QE(band_range)
print('QE in band' + str(band_range) + ' = ' + f'{QE_in_band:.5f}')

#%%

def draw_gaussian(ax, data,convert_to_photons=False):
    data -= np.min(data)
    data = data*electron_to_count
    if convert_to_photons:
        data *= QE_in_band
    pixels = np.arange(0, len(data))*pixel_length
    bounds_low = [np.max(data)*0.9, np.argmax(data)*0.9*pixel_length, 0.0001]
    bounds_high = [np.max(data)*1.1, np.argmax(data)*1.1*pixel_length, 0.01]
    opt, cov = curve_fit(gaussian, pixels, data, bounds=(bounds_low,bounds_high))
    cov = np.sqrt(np.diag(cov))

    fit = gaussian(pixels, opt[0], opt[1], opt[2])
    print('a = ' + F'{opt[0]:.2e}' + ' +- ' + F'{cov[0]:.2e}')
    print('x0 = ' + F'{opt[1]:.2e}' + ' +- ' + F'{cov[1]:.2e}')
    print('sigma = ' + F'{opt[2]:.2e}' + ' +- ' + F'{cov[2]:.2e}')
    print()
    
    ax.plot(pixels, data)
    ax.plot(pixels, fit)
    ax.grid(color='b', linestyle='-', linewidth=0.2)
    ax.set_xlim((0,pixels[-1]))
    ax.set_ylim(0, np.max(data)*1.1)
    
    f = InterpolatedUnivariateSpline(pixels, fit, k=1)
    low = opt[1] - opt[2]
    high = opt[1] + opt[2]
    calc = f.integral(low, high)
    print(calc)
  
    
x_data, y_data = get_pic(data_location + image0)    
  
fix, ax = plt.subplots(2)
draw_gaussian(ax[0], x_data, True)
draw_gaussian(ax[1], y_data, True)

plt.show()


#%%










