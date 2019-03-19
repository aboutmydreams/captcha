from PIL import Image
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from array import array
import os,sys
import numpy as np
import matplotlib.pyplot as plot




import make_captcha,solve_it

def get_my_train_img(times):
    for i in range(times):
        name,mig = make_captcha.get_train_img()
        mig = solve_it.clear_train_img(mig)
        mig.save('train_imgs/{}.png'.format(name))



