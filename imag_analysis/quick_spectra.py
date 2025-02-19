import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from skimage import io
from glob import glob
import matplotlib
matplotlib.rcParams.update({'errorbar.capsize': 4})

from image_processing import find_fov, offset_circular_mask

# filtAv = [438, 472, 500, 527, 549, 561, 568, 605, 631, 661, 692]
# filtUn = np.array([28, 35, 29, 22, 21, 21, 26, 22, 28, 26, 47]) / 2
filtAv = [438, 472, 549, 575, 586, 605, 631, 661, 676, 692]
filtUn = np.array([28, 35, 21, 35, 26, 22, 28, 26, 29, 47]) / 2
filtQE = np.array([0.52654585, 0.61510198, 0.67157561, 0.70026282, 0.71884383, 0.72505143, 0.72530424, 0.71414267, 0.68976776, 0.6438945])

def prepare_spectrum(files, roi = None):
    nfilt = len(files)
    
    img0 = io.imread(files[0]).astype(np.int64)
    imdark = io.imread(files[-1]).astype(np.int64)

    _, best_area, best_region = find_fov(img0, flag_plot=False)    # Refined FOV search on no_filter image
    
    circ_mask = offset_circular_mask(img, best_region, best_area, flag_plot=False)  # Rough (perfect) circular mask
    img0[~circ_mask] = 0
    imdark[~circ_mask] = 0
    imsize = circ_mask[circ_mask].shape    # Number of pixels in the circular mask
    # imsize = img0.shape[0] * img0.shape[1]
    
    if roi != None:
        imroi = img0[roi[0]:roi[1], roi[2]:roi[3]]
        imsize = imroi.shape[0] * imroi.shape[1]
    offset = 100 * imsize

    avInt = []
    unInt = []
    for i in range(nfilt-1):
        img = io.imread(files[i]).astype(np.int64)
        img[~circ_mask] = 0
        img = img - imdark

        if roi != None:
            img = img[roi[0]:roi[1], roi[2]:roi[3]]

        intPx = (img.sum() - offset) / imsize
        avInt.append(intPx)
        
        unPx = np.sqrt((img**2).sum()) / imsize
        unInt.append(unPx)

    avInt = np.array(avInt)
    unInt = np.array(unInt)
    cntQe = avInt / filtQE
    # cntQe /= (filtUn*2)

    unInt /= filtQE
    # unInt /= (filtUn*2)
    return cntQe, unInt


def plot_save_spectrum(path):
    # roi = [200, 1648, 600, 2048]
    roi = [400, 1300, 400, 1300]


    subdirs = [x[0] for x in os.walk(path)][1:]
    print('subdirs:')
    fig = plt.figure()
    for n,d in enumerate(subdirs):
        print(n+1, d)
        files = glob(d+'/*.tif')
        files.sort()
        c, un = prepare_spectrum(files, roi)
       
        plt.errorbar(x = filtAv, xerr=filtUn, y = c/(filtUn*2), yerr=un/(filtUn*2), fmt='o-', label=n+1)


    plt.gca().set(xlabel='$\lambda$ (nm)', ylabel='cnts/px/$\lambda$')
    plt.legend()
    plt.show()
    fig.savefig(path+'/quick_spectrum.png')

if __name__ == '__main__':
    path = sys.argv[1]
    plot_save_spectrum(path)