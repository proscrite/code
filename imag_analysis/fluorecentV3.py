# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 16:49:12 2022

@author: Nir Kapon
"""

import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches as patches
from scipy.optimize import curve_fit
# %matplotlib qt5

plt.rcParams['figure.figsize'] = [35,35]
plt.rcParams.update({'font.size':15})
directory = os.getcwd()
os.chdir(directory)
data_struct = np.dtype([('date', 'double'), ('power', 'double'), ('name', str), ('images', (np.uint16, (24, 2048, 2048)))])

Filters = \
    {
        1:  (np.NaN,np.NaN),
        2:  (438,28),
        3:  (472,35),
        4:  (500,29),
        5:  (527,22),
        6:  (549,21),
        7:  (561,21),
        8:  (586,26),
        9:  (605,22),
        10: (631,28),
        11: (661,26),
        12: (692,47)
    }
Filter_QE = \
    {
     2:     0.52654585,
     3:     0.61510198,
     4:     0.67157561,
     5:     0.70026282,
     6:     0.71884383,
     7:     0.72505143,
     8:     0.7279477,
     9:     0.72530424,
     10:    0.71414267,
     11:    0.68976776,
     12:    0.6438945 
    }
    
    
def filters_graphing(ax, means):    # create a better one...
    start = int(Filters[2][0] - (Filters[2][1]/2))
    end = int(Filters[12][0] + (Filters[12][1]/2))
    x = np.arange(start, end)
    y = np.ones(len(x))
    color = [0, 0, 1]
    for i in range(2,len(Filters)+1):
        filter_start = int(Filters[i][0] - (Filters[i][1]/2)) - start
        filter_end = int(Filters[i][0] + (Filters[i][1]/2)) - start
        indices = np.arange(filter_start, filter_end)
        subset = y[indices] * means[i-2]*0.8
        y[indices] = subset
        ax.plot(x, y, c=tuple(color))
        y = np.ones(len(x))
        color[0] += 0.1
        color[1] += 0.03
        color[2] += -0.1
     
    
    
#%%
data_folder = 'C:\\Users\\John\\My Drive\\Ba Tagging\\code\\microscope_control\\data\\numpy'

d23_05_23 = '\\23-05-23'
d29_05_23 = '\\29-05-23'

Bromobimane_H2O = '\\Bromobimane_H2O\\'
RuSL = '\\RuSL\\'
Bromobimane_Acetonitrile = '\\Bromobimane_Acetonitrile\\'

image_set0 = data_folder + d23_05_23 + Bromobimane_Acetonitrile + '3.npy'
image_set1 = data_folder + d23_05_23 + Bromobimane_Acetonitrile + '4.npy'
image_set2 = data_folder + d23_05_23 + Bromobimane_Acetonitrile + '5.npy'

image_set3 = data_folder + d29_05_23 + Bromobimane_Acetonitrile + '1.npy'

image_set4 = data_folder + d29_05_23 + Bromobimane_Acetonitrile + '2.npy'
image_set5 = data_folder + d29_05_23 + Bromobimane_Acetonitrile + '3.npy'
#moved location on the sample
image_set6 = data_folder + d29_05_23 + Bromobimane_Acetonitrile + '5.npy'
# reduce power
image_set7 = data_folder + d29_05_23 + Bromobimane_Acetonitrile + '6.npy'
image_set8 = data_folder + d29_05_23 + Bromobimane_Acetonitrile + '7.npy'
image_set9 = data_folder + d29_05_23 + Bromobimane_Acetonitrile + '8.npy'
image_set10 = data_folder + d29_05_23 + Bromobimane_Acetonitrile + '9.npy'

d01_06_23 = '\\01-06-23'
image_set_01_06 = []
for i in range(2, 10): # sets 0,1 were test ant are not useful for analisis
    image_set_01_06.append(data_folder + d01_06_23 + Bromobimane_Acetonitrile + str(i) + '.npy')

    
#%%
DEFAULT_CENTER_LOCATION = (525,749)
DEFAULT_BLOCK_SIZE = 2
def analisis_image_set(image_set_name, center_location=DEFAULT_CENTER_LOCATION, block_size=DEFAULT_BLOCK_SIZE, draw=False):
    image_set_data = np.load(image_set_name)
    image_set = image_set_data['images'][0][:]
    # dark_image = image_set_data['images'][0][12]
    # image_set = image_set_data['images'][0][:12]
    
    cut = 550
    center_block_x = center_location[0] + cut
    center_block_y = center_location[1] + cut
    #block_size = 2
    mean = np.zeros(24)
    
    corner_y = (int(center_block_x - block_size/2), int(center_block_x + block_size/2))
    corner_x = (int(center_block_y - block_size/2), int(center_block_y + block_size/2))
    w = np.zeros(11)
    for i in range(2,13):
        w[i-2] = Filters[i][0]
    
    # for i in range(len(blocks)):
    #     for j in range(len(blocks)):
    #         area = image_set[1:, corner_x[0] + blocks[i]:corner_x[1] + blocks[i], corner_y[0] + blocks[j]:corner_y[1] + blocks[j]]
    #         mean[i*len(blocks)+j] = np.mean(area, axis=(1,2))
            
    
    mean = np.mean(image_set[:,corner_x[0] : corner_x[1] + block_size, corner_y[0] : corner_y[1] + block_size], axis=(1,2))        
    
    if draw:
        fig_raw, ax_raw  = plt.subplots()
        #fig.tight_layout()
        ax_raw.plot(w, mean[13:24], linewidth=5, c=(0, 0, 0))
        ax_raw.plot(w, mean[1:12], c='b')
        ax_raw.plot(w, mean[1:12], 'o', c='b')
        ax_raw.grid(color='b', linestyle='-', linewidth=0.2)
        power = image_set_data['power'][0]
        title = 'raw data\nlaser power after sample: ' + f'{power}' +'[W]'
        ax_raw.set_title(title)
        ax_raw.set_xlabel('\u03bb [nm]')
        ax_raw.set_ylabel('Counts')
    
    raw = mean[1:12]
    
    
    
    mean[1:12] -= mean[13:24] # reduce dark rom normelaized data
    for i in range(2,13):
        mean[i-1] = mean[i-1]/Filters[i][1]
        mean[i-1] = mean[i-1]/Filter_QE[i]
        # reduce dark rom normelaized data so no need to normelize dark
        #mean[i-1 + 12] = mean[i-1 + 12]/Filters[i][1]
        #mean[i-1 + 12] = mean[i-1 + 12]/Filter_QE[i] 
        
    if draw:
        fig, ax  = plt.subplots()
        #fig.tight_layout()
        # reduce dark rom normelaized data so no need to show dark
        #ax.plot(w, mean[13:24], linewidth=5, c=(0, 0, 0)) 
        ax.plot(w, mean[1:12], c='b')
        ax.plot(w, mean[1:12], 'o', c='b')
        #filters_graphing(ax, mean[0])
        ax.grid(color='b', linestyle='-', linewidth=0.2)
        power = image_set_data['power'][0]
        title = 'normalized data\nlaser power after sample: ' + f'{power}' +'[W]'
        ax.set_title(title)
        ax.set_xlabel('\u03bb [nm]')
        ax.set_ylabel('Normelized counts')
        #ax.set_title()
        
        
        fig_12img, ax_12img = plt.subplots(3,4)
        fig_12img.tight_layout()
        
        
        for row in range(3):
            for col in range(4):
                area = image_set[col+row*4,cut:2048-cut,cut:2048-cut]
                img = ax_12img[row, col].imshow(area)
                #title = 'Filter center - ' + str(Filters[col+row*4+1][0]) + ', width - ' + str(Filters[col+row*4+1][1])
                title = str(Filters[col+row*4+1][0]) + '[nm], ' + str(Filters[col+row*4+1][1]) + '[nm]'
                #ax_12img[row, col].set_title('Filter center - ' + str(Filters[col+row*4][0]) + ', width - ' + str(Filters[col+row*4][0]))
                ax_12img[row, col].set_title(title)
                ax_12img[row, col].axis('off')
                fig_12img.colorbar(img, ax=ax_12img[row, col])
                rect = patches.Rectangle((center_block_x-cut, center_block_y-cut), block_size, block_size, linewidth=2, edgecolor='r',facecolor='none')
                ax_12img[row, col].add_patch(rect)
                # for i in range(len(blocks)):
                #     for j in range(len(blocks)):
                #         rect = patches.Rectangle((center_block_x + blocks[i]-cut, center_block_y + blocks[j]-cut), block_size, block_size, linewidth=1, edgecolor='r',facecolor='none')
                #         ax_12img[row, col].add_patch(rect)
    return mean[1:12] # raw

#%%

pixel_length = 6.5e-6
electron_to_count = 0.46
magnifacation = 25

def line(x, a, b):
    return a*x + b

p = np.zeros(len(image_set_01_06))
ratio = np.zeros(len(image_set_01_06))
counter = 0
for i in image_set_01_06:
    a = np.load(i)
    power = a['power'][0]
    image_set = a['images'][0][:]
    if np.max(image_set) < 65535:
        tot_pixels = np.sum(image_set[0,:,:])
        p[counter] = power
        ratio[counter] = power / tot_pixels
        counter += 1
p = p[0:counter-1]
ratio = ratio[0:counter-1]
fig, ax = plt.subplots()
arg, cov = curve_fit(line, p, ratio)
cov = np.sqrt(np.diag(cov))
p_range = np.linspace(- 0.2 *np.max(p), np.max(p), 100)
ax.plot(p_range, line(p_range, arg[0], arg[1]), '-')
#ax.semilogy(p, ratio, '*')
ax.plot(p, ratio, '*')
ax.grid(color='b', linestyle='-', linewidth=0.2)
ax.set_xlabel('power [W]')
ax.set_ylabel('power / sum_pixels')
plt.show()
#%%
analisis_location = [(477,757), (474,794), (480,788), (483,785), (492, 782), (493, 783), (500, 773), (503, 771), (493, 783)]
block_size = DEFAULT_BLOCK_SIZE + 2
pixels_area_of_analisis =  block_size**2 * pixel_length**2


w = np.zeros(11)
for i in range(2,13):
    w[i-2] = Filters[i][0]

fig_powers, ax_powers = plt.subplots()
ax_powers.grid(color='b', linestyle='-', linewidth=0.2)
ax_powers.set_xlabel('\u03bb [nm]')
ax_powers.set_ylabel('Normelized counts')
order = np.arange(0, len(image_set_01_06), 1)
powers = np.zeros(len(image_set_01_06))
counter = 0
for i in image_set_01_06:
    a = np.load(i)
    power = a['power'][0]
    image_no_filter = a['images'][0][0]
    
    cut = 550
    center_block_x = analisis_location[counter][0] + cut
    center_block_y = analisis_location[counter][1] + cut
    corner_y = (int(center_block_x - block_size/2), int(center_block_x + block_size/2))
    corner_x = (int(center_block_y - block_size/2), int(center_block_y + block_size/2))
    
    sum_area_pixels = np.sum(image_no_filter[corner_x[0] : corner_x[1] + block_size, corner_y[0] : corner_y[1] + block_size])
    power_on_pixels = line(power, arg[0], arg[1]) * sum_area_pixels
    power_on_sample = power_on_pixels * pixels_area_of_analisis / magnifacation
    means = analisis_image_set(i,center_location=analisis_location[counter], block_size=block_size, draw=False)
    label = f'{power_on_sample:.2e}' + r'$\left[\frac{W}{m^{2}}\right]$'
    ax_powers.plot(w, means, label=label)
    powers[counter] = power_on_sample
    
    counter += 1
    
def sort_array(x, y):
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]
    arrlinds = x.argsort()
    x = x[arrlinds[0::]]
    y = y[arrlinds[0::]]
    return x, y

powers, order = sort_array(powers, order)
handles, labels = ax_powers.get_legend_handles_labels()


ax_powers.legend([handles[idx] for idx in reversed(order)],[labels[idx] for idx in reversed(order)])

title = 'normalized data at diffrent iluminations'
ax_powers.set_title(title)
















