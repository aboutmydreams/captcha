from PIL import Image
import numpy as np
# np.set_printoptions(threshold=np.inf)


def get_small_modes(img,background=None):
    img = img.convert('L')
    box1 = (10, 4, 150, 36)
    img1 = img.crop(box1)
    mode = np.array(img1)
    if background:
        mode = np.where(mode < 100, 0, background)
    else:
        mode = np.where(mode < 100, 0, 1)
    return mode


def mode_to_img(mode,background=None):
    if background:
        mode = np.where(mode < 1, 0, background)
    array_mode = np.array(mode).astype('uint8')
    image = Image.fromarray(array_mode).convert('RGB')
    return image


def is_white_column(column):
    for c in column:
        if c == 0:
            return False
    return True


def vertical_cut(rect):
    last_position = 0
    c_position = 0
    width = rect.shape[1]

    result = []
    bools = []
    for x in range(width):
        c_position = x
        bools.append(is_white_column(rect[:, x]))
        if bools[-1] and (bools[-2] if bools.__len__() > 2 else True):
            last_position = c_position
        if bools[-1] and (not bools[-2] if bools.__len__() > 2 else True):
            if c_position - last_position >= 30:
                x1 = last_position
                x2 = int((c_position + last_position)/2)
                x3 = c_position
                print(x1, x2, x3)
                result.extend([rect[:, x1:x2], rect[:, x2:x3]])
            else:
                print(last_position, c_position)
                result.append(rect[:, last_position:c_position+1])
            last_position = c_position

    result.pop(0)
    result.pop(0)
    return result



img7 = Image.open('8.png')
my_mode = get_small_modes(img7)

li = vertical_cut(my_mode)
for i in li:
    img = mode_to_img(i,255)
    img.show()
