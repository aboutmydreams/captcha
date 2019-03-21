from PIL import Image
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
import matplotlib.pyplot as plt
from array import array
import os,sys
import numpy as np



import make_captcha,solve_it

def get_my_train_img(times):
    for i in range(times):
        name,mig = make_captcha.get_train_img()
        mig = solve_it.clear_train_img(mig)
        mig.save('train_imgs/{}.png'.format(name))


def get_xy():
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    

    train_img_path = 'train_imgs/'
    test_img_path = 'test_imgs/'
    data_list = os.listdir(train_img_path)
    data_list1 = os.listdir(test_img_path)
    for file in data_list:
        if file != '.DS_Store':
            img = Image.open(train_img_path + file)
            x = make_captcha.get_mode(img)
            x_train.append(x)
            y_train.append(ord(file[0]))

    for file in data_list1:
        if file != '.DS_Store':
            img = Image.open(test_img_path + file)
            x = make_captcha.get_mode(img)
            x_test.append(x)
            y_test.append(ord(file[0]))
    return map(np.array,[x_train,y_train,x_test,y_test])


# x_train,y_train,x_test,y_test = get_xy()
# a = np.array([x_train,y_train,x_test,y_test])
# np.save("npmode/xytt.npy",a)

x_train,y_train,x_test,y_test = np.load("npmode/xytt.npy").tolist()
print(x_train[0].shape)


classes = 26
batch_size = 1
epochs = 20

'''

# 全连接模型
model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(32,30)))
# model.add(Dropout(0.2))
# model.add(Dense(512, activation='relu'))
# model.add(Dropout(0.2))
model.add(Dense(classes, activation='softmax'))

model.summary()

#损失函数使用交叉熵
model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])
#模型估计
model.fit(x_train, y_train, epochs=5, batch_size=32)
score = model.evaluate(x_test, y_test, verbose=0)
print('Total loss on Test Set:', score[0])
print('Accuracy of Testing Set:', score[1])

'''