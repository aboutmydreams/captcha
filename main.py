from PIL import Image
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop,SGD
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
            y_train.append(ord(file[0])-65)

    for file in data_list1:
        if file != '.DS_Store':
            img = Image.open(test_img_path + file)
            x = make_captcha.get_mode(img)
            x_test.append(x)
            y_test.append(ord(file[0])-65)
    return map(np.array,[x_train,y_train,x_test,y_test])


# x_train,y_train,x_test,y_test = get_xy()
# a = np.array([x_train,y_train,x_test,y_test])
# np.save("npmode/xytt.npy",a)

x_train,y_train,x_test,y_test = np.load("npmode/xytt.npy").tolist()
x_train = x_train.reshape(x_train.shape[0],-1)
x_test = x_test.reshape(x_test.shape[0],-1)
print(x_train.shape,y_train.shape)
print(y_train)



y_train = np_utils.to_categorical(y_train,num_classes=26)
y_test = np_utils.to_categorical(y_test,num_classes=26)



# 全连接模型
model = Sequential()
model.add(Dense(units=256,input_dim=960,bias_initializer='one',activation='tanh'))
model.add(Dropout(0.2))
model.add(Dense(units=128,activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(units=26,activation='softmax'))

model.summary()

# 损失函数使用交叉熵
sgd = SGD(lr=0.1)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])
#模型估计
model.fit(x_train, y_train, epochs=50, batch_size=64)
loss,accuracy = model.evaluate(x_test,y_test)
print('loss:',loss)
print('accuracy:',accuracy)

model.save('model.h5')
