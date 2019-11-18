#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 15:52:10 2019

@author: ghadir
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt
from skimage.segmentation import mark_boundaries

def normalize(img):
    maxi=np.max(img)
    mini=np.min(img)
    img = (img - mini)/(maxi-mini)
    return img


while True:
    patient_number = input("Enter patient number or x to break: ")
    print('In while loop')
    
    try:
        print('In try')
        
        if patient_number == 'x':
            break
        elif int(patient_number)<100:
            patient_number = '0' + patient_number
        
        file_name = 'R01-' + patient_number +'.pickle'
        with open(file_name, 'rb') as f:
            patient = pickle.load(f)
            print("In open")
            print(type(patient['mask']))
            tags=patient['tags']
            print(tags['PatientID'])
        
        img = patient['img']
        mask = patient['mask']
        
        img = normalize(img)
        
        for i in range (mask.shape[0]):
            #print('In for loop', -i+1)
            if (mask[i].any()==1):
                print("In if")
                #new_img = np.rot90(np.rot90(np.rot90(img[i])))
                #plt.imshow(mark_boundaries(new_img, mask[i]>0.01, color=(1,0,0)), 'gray')
                #plt.subplot(121).imshow(img[i])
                #plt.subplot(122).imshow(mask[i])
                #plt.show()
                img1=img[i]
                img2=mask[i]
                #f, (ax) = plt.subplots(1, 1, figsize=(20,10),sharey=True)
                #ax.grid(False)
                #ax.imshow(mark_boundaries(img1, img2>0.01, color=(1, 0, 0)),'gray')
                #plt.show()
                
    except:
        print("Invalid input")

    
