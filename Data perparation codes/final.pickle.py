#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 11:50:52 2019

@author: ghadir
"""

import pickle
import numpy as np
import pydicom as pyd
from tqdm import tqdm
import glob
import matplotlib.pyplot as plt
import os
import json

#%% Helper functions:

def get_tags(patient):
    tags = {}
    tags_lst = patient.dir("")
    for tag in tags_lst:
        if tag == 'PixelData':
            continue
            print("Didn't continue")
        tags[tag] = str(patient.data_element(tag).value)
    return dict(tags)

#############################################################################
    
def read_patient (path_to_annotation, path_to_patient):
    lst = glob.glob(path_to_patient+'/*.dcm')
    #print(lst[:5])
    patient = [pyd.read_file(f) for f in lst]
    patient = sort_slices(patient)
    
    tumor = pyd.read_file(path_to_annotation)
    annotation = make_annotation(tumor, patient)
    
    return annotation

############################################################################
    
def sort_slices (slices_lst):
    sorted_slices = [] 
    for i in range (len(slices_lst)+1):
        for j in range (len(slices_lst)):
            if (slices_lst[j][0x20, 0x13].value == i+1):
                sorted_slices.append(slices_lst[j])
        
    
    return sorted_slices
    
############################################################################
    
def make_annotation(tumor, patient):
    new_shape = (len(patient),512,512)
    annotation = np.zeros(new_shape)
    begining = tumor.ReferencedSeriesSequence[0][0x08, 0x114a][0][0x08, 0x1155].value
    
    for Slice in range(len(patient)):
        if (begining == patient[Slice].SOPInstanceUID):
            print("\nFound it before %d ! \n"%Slice)
            for i, tumor_slice in enumerate(tumor.pixel_array):
                annotation[-Slice+i-1,:,:]= tumor_slice
            break
    
        
    return annotation

#%% Main program:

def main():
    old_loc = '/home/ghadir/NSCLC dataset/'
    
    loc_img = 'Patients/*.dcm'
    
    loc_mask_default = 'Annotations/*.dcm'
    loc_mask_old = '/home/ghadir/Downloads/Radiogenomics dataset/NSCLC_DICOM_2017/NSCLC Radiogenomics/'
    
    patients_lst = glob.glob(old_loc + loc_img)
    masks_lst = glob.glob(old_loc + loc_mask_default)
    
    patients_lst.sort()
    masks_lst.sort()
    
    masks_lst = masks_lst[:96]
    helper_patients_lst = []
    
    to_be_changed = []
    
    new_loc = '/home/ghadir/pickled NSCLC/'
    
    with open ('pathes.txt') as f:
        for line in f:
            patient_name = line[:7]
            to_be_changed.append(patient_name)
            path= loc_mask_old + line.rstrip()
            subpathes = glob.glob(path+'/*')
            for i in subpathes:
                if '1000-ePAD' in i:
                    path = (i+'/000000.dcm')
                    masks_lst.append(path)
                else:
                    helper_patients_lst.append(i)
            
            
    #for i in range (len(masks_lst)):
     #   print(masks_lst[i], '\n\n')
    
        
    for i, patient_loc in enumerate(patients_lst): #96
        print(patient_loc)
        patient = {}
        patient_name = patient_loc[-11:-4] + '.dcm'
        mask_loc = masks_lst[i]
        print(mask_loc)
        location = new_loc + patient_name[:-4] + '.pickle'
        if patient_name[:-4] in to_be_changed:
            #print(i-96)
            patient_mask = read_patient(mask_loc, helper_patients_lst[i-96])
            print(helper_patients_lst[i-96])
        else:
            patient_mask = pyd.read_file(mask_loc)
            patient_mask = np.copy(patient_mask.pixel_array)
        
        print('\n')
        
        patient_file = pyd.read_file(patient_loc)
        patient_tags = get_tags(patient_file)
        patient_img = np.copy(patient_file.pixel_array)
        
        patient['tags'] = patient_tags
        patient['img']  = patient_img
        patient['mask'] = patient_mask
        
        #mass_boundries=[]
        #for i in range (patient_mask.shape[0]):
         #   if (patient_mask[i].any()==1):
         #       mass_boundries.append(i)
        #print(len(mass_boundries))
        #print(mass_boundries[0], mass_boundries[-1])
        
        #np.save(location, patient)
        
        with open (location, 'wb+') as f:
            pickle.dump(patient, f)
        
"""
        with open(location, 'w+') as f:
            json.dump(str(patient), f)
            print(type(str(patient)))
        print('Ok')
            
        break
"""        
        
        
    
"""
    for i, patient in enumerate(patients_lst):
        patient_name = masks_lst[i][:7]
        if patient_name in to_be_chnaged:
            masks_lst[i] = 
    """

#%% Run program:
    
main()
#print(pickle.DEFAULT_PROTOCOL)