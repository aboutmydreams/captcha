from PIL import Image
from collections import Counter

import numpy as np

def get_modes(img):
    img = img.convert('L')
    mode = np.array(img)
    mode = np.where(mode < 100, 0, 1)
    return mode

cut_time = 0
img1 = Image.open('de_crook_imgs/3.png')
mode = get_modes(img1)
new_mode = []
column = 0
dividing_line = []
while len(dividing_line) < 4:
    if (1 in mode.T[column]):
        dividing_line.append(column)
        column += 1
        print(column)
print(dividing_line)
        
        

