from PIL import Image
from collections import Counter

import numpy as np

# 保证所有数据能够显示，而不是用省略号表示
np.set_printoptions(threshold = np.inf) 

def get_modes(img):
    mode = np.asarray(img)
    mode = np.where(mode < 100, 0, 1)
    return mode

# N 干扰线纵向像素点个数
def clear_line(image):
    # 0和1互相转换
    def one_zero(num):
        if num == 1:
            return 0
        else:
            return 1
    t2val = {}
    t2val[(0, 0)] = 1
    t2val[(image.size[0] - 1, image.size[1] - 1)] = 1

    mode = get_modes(image)
    new_mode = []
    for line in mode.T:
        new_column = is_three0(line)
        new_mode.append(list(new_column))
    new_mode = eval(str(new_mode).replace('1','[255,255,255]').replace('0','[0,0,0]'))
    print(new_mode)
    image = Image.fromarray(np.array(new_mode).T.astype('uint8'))
    image.show()



# 判断列表中连续的三个位置是否是0,且相邻位置是1，替换掉这3个0
def is_three0(column, N):
    column_str = ''.join(column)
    zero_site_list = [i for i,v in enumerate(column) if v==0]
            # if (column[i-1]==0) and (column[i+1]==0) and (column[i-2]==1) and (column[i+2]==1):
                # column[i+1],column[i+2],column[i+3]=1,1,1
    return column


img1 = Image.open('resultimgs/1.png')
mode1 = get_modes(img1)

clear_line(img1)