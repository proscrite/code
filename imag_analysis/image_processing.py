import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from skimage import io, color, filters, morphology, measure

def find_fov(gray_image):
    """Finding the field of view in a gray image. This will be the disk with the largest area and solidity.
    Args: gray_image: 2D numpy array representing the gray image.
    Returns: fov_mask: 2D numpy array representing the binary mask of the field of view.
    
    """

    # Apply thresholding to create a binary mask
    threshold = filters.threshold_otsu(gray_image)
    print('Threshold otsu: ', threshold)
    binary_mask = gray_image > threshold

    # Perform morphological closing to fill small gaps
    binary_mask = morphology.closing(binary_mask, morphology.disk(10))

    # Label connected components
    labeled_mask = measure.label(binary_mask)

    # Measure properties of labeled regions
    regions = measure.regionprops(labeled_mask)

    # Find the largest circular region based on area and solidity
    best_region = None
    best_circularity = 0

    for region in regions:
        area = region.area
        perimeter = region.perimeter if region.perimeter > 0 else 1
        circularity = 4 * np.pi * (area / (perimeter ** 2))
        
        if circularity > best_circularity and area > 1000:  # Ignore small noise
            best_circularity = circularity
            best_region = region
            best_area = area


    # Create a mask for the detected FOV
    fov_mask = np.zeros_like(binary_mask, dtype=bool)

    if best_region:
        fov_mask[labeled_mask == best_region.label] = True
    return fov_mask, best_area, best_region

def offset_circular_mask(img, best_region, best_area, flag_plot = True):
    """Create a circular mask based on the detected region.
    args: 
          img: 2D numpy array representing the image.
          best_region: regionprops object representing the detected region.
          best_area: int representing the area of the detected region.
          flag_plot: bool to display the mask.
    returns:
          circular_mask: 2D numpy array representing the circular
            mask centered on the detected region
    """
    # Extract the centroid (regionprops returns (row, col))
    center_y, center_x = best_region.centroid  

    # Use the known or calculated radius, e.g. from area = πr²:
    # radius ≈ sqrt(area / π). If your area is ~2,625,898:
    fixed_radius = int(np.sqrt(best_area / np.pi))

    # Create a coordinate grid
    height, width = img.shape
    Y, X = np.ogrid[:height, :width]

    # Build the circular mask. This will be True inside the circle.
    circular_mask = (X - center_x)**2 + (Y - center_y)**2 <= fixed_radius**2
    # Display the mask
    if flag_plot:
        plt.figure(figsize=(8, 6))
        plt.imshow(circular_mask, cmap='gray')
        plt.title("Offset Circular Mask (Partially Outside Image)")
    return circular_mask



def prepare_spectrum(files, roi = None):
    nfilt = len(files)
    
    img0 = io.imread(files[0]).astype(np.int64)
    fov, best_area, best_region = find_fov(img0, flag_plot=False)    # Refined FOV search
    
    circ_mask = offset_circular_mask(img, best_region, best_area, flag_plot=False)  # Rough (perfect) circular mask
    img0[~circ_mask] = 0
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