import numpy as np
import pydicom as pyd
import matplotlib.pyplot as plt
import glob

def show_dcm (location):

    Is_ok = 1
    lst = glob.glob(location+"/*.dcm")
    lst.sort()
    Range = np.arange(len(lst))
    patient = [pyd.read_file(f) for f in lst]
    patient = sort_slices(patient) #Added


    while Is_ok:
        Slice = input("Enter slice number in range {}, or 'x' to break: ".format(len(lst)))
        if Slice == 'x':
            break
        elif int(Slice) in Range:
            img = patient[int(Slice)]
#            img = pyd.dcmread(lst[int(slice)])
            print(img[0x20, 0x13])
            plt.imshow(img.pixel_array, 'gray')
            plt.show()
        else:
            Slice = input("Invalid input, pls enter a value in range {} or 'x'".format(len(lst)))

def sort_slices (slices_lst):
    sorted_slices = []
    
    for i in range (len(slices_lst)+1):
        for j in range (len(slices_lst)):
            if (slices_lst[j][0x20, 0x13].value == i+1):
                print(slices_lst[j][0x20, 0x13].value)
                sorted_slices.append(slices_lst[j])
        
    
    return sorted_slices