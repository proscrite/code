import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from skimage import io
from glob import glob
import matplotlib
matplotlib.rcParams.update({'errorbar.capsize': 4})

filtAv = [438, 472, 500, 527, 549, 561, 568, 605, 631, 661, 692]
filtUn = np.array([28, 35, 29, 22, 21, 21, 26, 22, 28, 26, 47]) / 2
filtQE = np.array([0.52654585, 0.61510198, 0.67157561, 0.70026282, 0.71884383, 0.72505143, 0.7279477, 0.72530424, 0.71414267, 0.68976776, 0.6438945])
roi = [750, 1350, 400, 1000]
N = 400

def temporal_evolution(files,N=400,roi=[0,512,0,512]):
    im0 = io.imread(files[0]).astype(np.int64)[roi[0]:roi[1], roi[2]:roi[3]]
    data0=np.zeros_like(im0)
    data=np.stack((data0,im0))
    for i in range (2,N):
        d=io.imread(files[i]).astype(np.int64)[roi[0]:roi[1], roi[2]:roi[3]]
        data=np.append(data,[d],axis=0)
    data=np.delete(data,0,0)
    return data


def average_tevol(data):
    I, J = np.shape(data[0])
    av_evol = np.zeros_like(data[:, 0, 0])
    for i in range(I):
        for j in range(J):
            av_evol += data[:, i, j]
    av_evol = av_evol/(I*J)

    return av_evol


def plot_save_trajectories(path, Nexp = None):

    subdirs = [x[0] for x in os.walk(path)][1:]
    colors = ['b', 'orange', 'g', 'r']
    print('subdirs:', subdirs)
    fig = plt.figure()

    if Nexp == None:
        for n,d in enumerate(subdirs):
            print(n, d)
            files = glob(d+'/*.tif')
            files.sort()
            data = temporal_evolution(files, N, roi)
            av_evol = average_tevol(data)

            plt.plot(av_evol, 'o', label='Experiment '+str(n+1))
        
        plt.gca().set(xlabel='t (s)', ylabel='I/px') # ,ylim=(5000, 6500) )
        plt.legend()
        plt.show()
        fig.savefig(path+'/av_trajectories.png')
    
    else:
        d = subdirs[Nexp-1]
        files = glob(d+'/*.tif')
        files.sort()
        data = temporal_evolution(files, N, roi)
        av_evol = average_tevol(data)

        plt.plot(av_evol, 'o', color=colors[Nexp-1], label='Experiment '+str(Nexp))
        plt.gca().set(xlabel='t (s)', ylabel='I/px') # ,ylim=(5000, 6500) )
        plt.legend()
        plt.show()
        fig.savefig(path+'/av_trajectory_%i.png' %Nexp)

if __name__ == '__main__':
    path = sys.argv[1]
    if len(sys.argv) > 2:
        Nexp = int(sys.argv[2])
    else: Nexp = None
    plot_save_trajectories(path, Nexp)

