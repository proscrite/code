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
#%%

B1_loction = 'C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\B1_RuSL\\'
B1_files = ['center_0.00017922[W].npy', 'E_7.5222e-06[W].npy', 'N_3.7009e-06[W].npy', 'NE_4.1233e-06[W].npy', 'S_4.2659e-05[W].npy', 'W_0.00034067[W].npy', 'center_dark.npy']
B1_centers = [(532,607),(792,600),(569,413),(654,445),(578,817),(382,606)]
# [2] maby seeing something    
    
#%%
Old_06ND = "old\\08-12-22_16-47-34.npy"
No_laser = "old\\15-12-22_14-52-11.npy"
Mesurments = \
    {
        0:  "C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\15-12-22_13-26-15.npy",
        1:  "C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\15-12-22_14-33-03.npy",
        2:  "C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\15-12-22_14-22-04.npy",
        3:  "C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\15-12-22_14-28-12.npy",
        4:  "C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\15-12-22_13-22-37.npy",
        6:  "C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\15-12-22_12-58-54.npy",
        8:  "C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\15-12-22_13-04-26.npy",
        10: "C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\15-12-22_13-14-45.npy",
        16: "C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\15-12-22_13-09-40.npy",
        1000:"C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\15-12-22_14-43-41.npy",
    }

Mesurments_V2_Location = 'C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\data\\V2\\'
Mesurments_V2 = \
    {
        0:  "old\\29-12-22_17-23-00_8.9632e-05[W].npy",
        1:  "old\\29-12-22_17-19-40_7.1882e-05[W].npy",
        2:  "old\\29-12-22_17-17-40_5.9862e-05[W].npy",
        3:  "old\\29-12-22_17-14-41_4.9588e-05[W].npy",
        4:  "old\\29-12-22_17-27-28_3.2447e-05[W].npy",
        5:  "old\\29-12-22_16-47-22_2.5259e-05[W].npy",
        6:  "old\\29-12-22_17-30-10_1.9762e-05[W].npy",
        7:  "old\\29-12-22_17-09-27_1.7048e-05[W].npy",
        8:  "old\\29-12-22_17-32-00_1.3458e-05[W].npy",
        9:  "old\\29-12-22_16-57-12_9.0408e-06[W].npy",
        10: "old\\29-12-22_17-33-50_7.1281e-06[W].npy",
        11: "old\\29-12-22_17-24-30_5.5397e-06[W].npy",
        20: "old\\29-12-22_17-11-56_3.641e-07[W].npy",
        30: "old\\29-12-22_17-35-43_7.9114e-08[W].npy",
        40: "old\\29-12-22_17-37-47_4.4835e-08[W].npy",
    }
test1 = 'C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\data\\test1\\02-01-23_14-59-22_0.0041711[W].npy'   
test2 = 'C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\data\\12_01_23\\12-01-23_16-33-28_0.0011713[W].npy' 
test3 = 'C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\data\\16-01-23_13-17-50_0.00085746[W].npy'
diffuser1 = 'C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\data\\test1\\23-01-23_13-47-12.npy'
test4 = 'C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\data\\test1\\26-01-23_12-10-31_7.0468e-06[W].npy'
test5 = 'C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\data\\test1\\26-01-23_13-22-19_0.00072095[W].npy'
test6 = 'C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\data\\test1\\26-01-23_14-14-35_0.00058774[W].npy'
test7 = 'C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\old\\data\\test1\\26-01-23_15-15-56_0.0005741[W].npy'

dark_test1 = "C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\data\\dark_issue\\16-02-23_12-21-24_0.00011885[W].npy" # with laser
dark_test2 = "C:\\Users\\John\\Documents\\ba_tagging\\imag_analisis\\data\\dark_issue\\16-02-23_12-22-06_4.7694e-10[W].npy" # without laser

#%%
image_set = np.load(Mesurments[0])
x_corner = 750
y_corner = 1150
size = 48
blocks_x = np.arange(start=-4, stop=5, step=1)*size + x_corner
blocks_y = np.arange(start=-4, stop=5, step=1)*size + y_corner
mean = np.zeros((18,11))

for i in range(len(blocks)):
    mean[i] = np.mean(image_set[1:,blocks_x[i]:blocks_x[i]+size,y_corner:y_corner+size], axis=(1,2))
    
for i in range(len(blocks)):
    mean[i+9] = np.mean(image_set[1:,x_corner:x_corner+size,blocks_y[i]:blocks_y[i]+size], axis=(1,2))    

w = np.zeros(11)
for i in range(2,13):
    w[i-2] = Filters[i][0]
    for j in range(18):
        mean[j][i-2] = mean[j][i-2]/Filters[i][1]
    
    
fig, ax  = plt.subplots()
for j in range(18):
    ax.plot(w,mean[j])



fi1, ax1 = plt.subplots()
ax1.imshow(image_set[11])
for i in range(9):
    rect = patches.Rectangle((blocks_x[i]+size/2,y_corner+size/2), size, size, linewidth=1, edgecolor='r',facecolor='none')
    ax1.add_patch(rect)
for i in range(9):
    rect = patches.Rectangle((x_corner+size/2,blocks_y[i]+size/2), size, size, linewidth=1, edgecolor='r',facecolor='none')
    ax1.add_patch(rect)
#%%
x_corner = 750
y_corner = 1150
size = 48
mean = np.zeros((len(Mesurments),11))
fig, ax  = plt.subplots()
index = 0

w = np.zeros(11)
for i in range(2,13):
    w[i-2] = Filters[i][0]
    

for i in Mesurments:
    image_set = np.load(Mesurments[i]) - np.load(Mesurments[1000])
    mean[index] = np.mean(image_set[1:,x_corner:x_corner + size,y_corner:y_corner + size], axis=(1,2))
    for j in range(11):
        mean[index][j] = mean[index][j]/Filters[j+2][1]
    label = F'${i*0.1:.1f}$' + 'ND'
    ax.plot(w,mean[index],label=label)
    index += 1

ax.grid(color='b', linestyle='-', linewidth=0.2)
ax.set_xlabel('\u03bb [nm]')
ax.set_ylabel('Intensity [counts]')    
ax.legend()    

#%%
fig_12img, ax_12img = plt.subplots(3,4)
image_set = np.load(diffuser1)
cut = 0
for row in range(3):
    for col in range(4):
        area = image_set[col+row*4,cut:2048-cut,cut:2048-cut]
        img = ax_12img[row, col].imshow(area)
        print(np.unravel_index(np.argmax(area), area.shape) , str(np.amax(area)))
        ax_12img[row, col].axis('off')
        title = 'Filter center - ' + str(Filters[col+row*4+1][0]) + ', width - ' + str(Filters[col+row*4+1][1])
        ax_12img[row, col].set_title(title)
        fig_12img.colorbar(img, ax=ax_12img[row, col])

#%%

#image_set = np.load(Mesurments_V2_Location+Mesurments_V2[0])
#image_set = np.load(B1_loction + B1_files[5])
image_set = np.load(dark_test1)

cut = 550
center_block_x = 537+cut
center_block_y = 595+cut
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



w = np.zeros(11)
for i in range(2,13):
    w[i-2] = Filters[i][0]
    for j in range(num_of_blocks):
        mean[j][i-2] = mean[j][i-2]#/Filters[i][1]
        
        

fig, ax  = plt.subplots()
#fig.tight_layout()
for j in range(num_of_blocks):
    ax.plot(w,mean[j],label=('Block: ' + str(j)))
ax.grid(color='b', linestyle='-', linewidth=0.2)
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

