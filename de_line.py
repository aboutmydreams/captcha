from PIL import Image
from collections import Counter

import numpy as np

# 保证所有数据能够显示，而不是用省略号表示
np.set_printoptions(threshold = np.inf) 

def get_modes(img):
    mode = np.array(img)
    mode = np.where(mode < 100, 0, 1)
    return mode

# N 干扰线纵向像素点个数
def clear_line(image, N):
    # 0和1互相转换
    t2val = {}
    t2val[(0, 0)] = 1
    t2val[(image.size[0] - 1, image.size[1] - 1)] = 1

    mode = get_modes(image)
    new_mode = []
    for line in mode.T:
        new_column = is_three0(line,N)
        new_mode.append(new_column)

    new_mode = eval(str(new_mode).replace('1','255').replace('0','0'))
    image = Image.fromarray(np.array(new_mode).T.astype('uint8')).convert('RGB')
    return image



# 判断列表中连续的三个位置是否是0,且相邻位置是1，替换掉这3个0
def is_three0(column, N):
    column_str = ''.join(map(str,column))
    zero_site_list = [i for i,v in enumerate(column) if v==0]

    for i in  zero_site_list[-N:]:
        if i > len(column)-N-1:
            zero_site_list.remove(i)

    for i in zero_site_list:
        if i > 0 and column_str[i:i+N] == '0' * N and column_str[i+N] == '1' and column_str[i-1] == '1':
            column_str = column_str[:i] + '1' * N + column_str[i+N:]
    column = list(map(int,column_str))
    return column

for i in range(1,50):
    img1 = Image.open('resultimgs/{}.jpeg'.format(str(i)))
    # print(is_three0(mode1.T[1], 3))
    img2 = clear_line(img1,3)
    img3 = clear_line(img2.convert('L'),4)
    img3.save('lastimgs/{}.png'.format(str(i)))
print(get_modes(Image.open('de_line_imgs/2.png')))