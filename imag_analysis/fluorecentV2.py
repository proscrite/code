# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 16:49:12 2022

@author: Nir Kapon
"""

import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches as patches


plt.rcParams['figure.figsize'] = [35,35]
plt.rcParams.update({'font.size':15})
directory = os.getcwd()
os.chdir(directory)
data_struct = np.dtype([('date', 'double'), ('power', 'double'), ('name', str), ('images', (np.uint16, (13, 2048, 2048)))])
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
    for i in range(2,len(Filters)+1):
        filter_start = int(Filters[i][0] - (Filters[i][1]/2)) - start
        filter_end = int(Filters[i][0] + (Filters[i][1]/2)) - start
        indices = np.arange(filter_start, filter_end)
        subset = y[indices] * means[i-2]*0.8
        subset[subset > means[i-2]*0.8] = (means[i-2] + means[i-3])*0.8/2
        y[indices] = subset
    y -= 1
    ax.plot(x, y, c='y')
    
    
#%%

location = 'C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\data\\'
d23_02_23 = location + '\\23-02-23\\RuSL\\'
test0 = d23_02_23 + '0.npy'
test1 = d23_02_23 + '1.npy'
test2 = d23_02_23 + '2.npy'
test3 = d23_02_23 + '3.npy'

d04_04_23 = location + '\\04-04-23\\Card\\'
card_test0 = d04_04_23 + '0.npy' # bad imaging (complitly saturated)
card_test1 = d04_04_23 + '1.npy' # bad imaging (laser was covered)
card_test2 = d04_04_23 + '2.npy'

d01_05_23 = location + "\\01-05-23\\Bromobimane\\"
Bromobimane0 = d01_05_23 + '0.npy'
Bromobimane1 = d01_05_23 + '1.npy'

d02_05_23 = location + "\\02-05-23\\Bromobimane\\"
Bromobimane1_0 = d02_05_23 + '0.npy'
Bromobimane1_1 = d02_05_23 + '1.npy'
Bromobimane1_2 = d02_05_23 + '2.npy'
Bromobimane1_3 = d02_05_23 + '3.npy'
Bromobimane1_4 = d02_05_23 + '4.npy'

d02_05_23_type2 = location + "\\02-05-23\\Bromobimane_type2\\"
Bromobimane_type2_0 = d02_05_23_type2 + '0.npy'
    
#%%

image_set_data = np.load(Bromobimane_type2_0)
dark_image = image_set_data['images'][0][12]
image_set = image_set_data['images'][0][:12]

cut = 550
center_block_x = 406+cut
center_block_y = 746+cut
block_size = 2
blocks = np.array([-block_size, 0, block_size])
num_of_blocks = len(blocks)**2
mean = np.zeros((num_of_blocks,11))

corner_y = (int(center_block_x - block_size/2), int(center_block_x + block_size/2))
corner_x = (int(center_block_y - block_size/2), int(center_block_y + block_size/2))


for i in range(len(blocks)):
    for j in range(len(blocks)):
        area = image_set[1:, corner_x[0] + blocks[i]:corner_x[1] + blocks[i], corner_y[0] + blocks[j]:corner_y[1] + blocks[j]]
        mean[i*len(blocks)+j] = np.mean(area, axis=(1,2))

dark = np.mean(dark_image[cut:2048-cut,cut:2048-cut])*np.ones(11)

w = np.zeros(11)
for i in range(2,13):
    w[i-2] = Filters[i][0]
    for j in range(num_of_blocks):
        mean[j][i-2] = mean[j][i-2]/Filters[i][1]
        mean[j][i-2] = mean[j][i-2]/Filter_QE[i]
        
        

fig, ax  = plt.subplots()
#fig.tight_layout()
ax.plot(w,dark)
for j in range(num_of_blocks):
    ax.plot(w,mean[j],label=('Block: ' + str(j)))
filters_graphing(ax, mean[0])
ax.grid(color='b', linestyle='-', linewidth=0.2)
power = image_set_data['power'][0]
title = f'{power}' +'[W]'
ax.set_title(title)
ax.set_xlabel('\u03bb [nm]')
ax.set_ylabel('Intensity [counts]')
#ax.set_title()

#fig1, ax1 = plt.subplots()
#fig1.tight_layout()
#ax1.imshow(image_set[6])
#for i in range(len(blocks)):
#    for j in range(len(blocks)):
#        rect = patches.Rectangle((center_block_x + blocks[i], center_block_y + blocks[j]), block_size, block_size, linewidth=1, edgecolor='r',facecolor='none')
#        ax1.add_patch(rect)

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
        
        for i in range(len(blocks)):
            for j in range(len(blocks)):
                rect = patches.Rectangle((center_block_x + blocks[i]-cut, center_block_y + blocks[j]-cut), block_size, block_size, linewidth=1, edgecolor='r',facecolor='none')
                ax_12img[row, col].add_patch(rect)

#%%

data_set0 = np.load(test0)
data_set1 = np.load(test1)
data_set2 = np.load(test2)
data_set3 = np.load(test3)

cut = 550
center_block_y = 633+cut
center_block_x = 564+cut
size = 1

power = np.zeros(4)
power[0] = data_set0['power'][0]
power[1] = data_set1['power'][0]
power[2] = data_set2['power'][0]
power[3] = data_set3['power'][0]

mean = np.zeros(4)
filter_ = 10


area0 = data_set0['images'][0][filter_,center_block_x-size:center_block_x+size,center_block_y-size:center_block_y+size]
area1 = data_set1['images'][0][filter_,center_block_x-size:center_block_x+size,center_block_y-size:center_block_y+size]
area2 = data_set2['images'][0][filter_,center_block_x-size:center_block_x+size,center_block_y-size:center_block_y+size]
area3 = data_set3['images'][0][filter_,center_block_x-size:center_block_x+size,center_block_y-size:center_block_y+size]

mean[0] = np.mean(area0)
mean[1] = np.mean(area1)
mean[2] = np.mean(area2)
mean[3] = np.mean(area3)

fig1, ax1  = plt.subplots()

ax1.plot(power,mean)
ax1.plot(power,mean, 'o')
title = str(Filters[filter_+1][0]) + '[nm], ' + str(Filters[filter_+1][1]) + '[nm]'
ax1.set_title(title)
ax1.set_xlabel('power [W]')
ax1.set_ylabel('Intensity [counts]')
ax1.grid(color='b', linestyle='-', linewidth=0.2)






















