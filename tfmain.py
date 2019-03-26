import tensorflow as tf
import numpy as np
import os
from PIL import Image

import make_captcha,solve_it

FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_integer("is_train", 1, "指定程序是预测还是训练")


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


def full_connected():
    # 获取真实的数据
    x_train,y_train,x_test,y_test = get_xy()

    # 1、建立数据的占位符 x [None, 784]    y_true [None, 10]
    with tf.variable_scope("data"):
        x = tf.placeholder(tf.float32, [None, 960])
        y_true = tf.placeholder(tf.int32, [None, 26])

    # 2、建立一个全连接层的神经网络 w [784, 10]   b [10]
    with tf.variable_scope("fc_model"):
        # 随机初始化权重和偏置
        weight = tf.Variable(tf.random_normal([960, 26], mean=0.0, stddev=1.0), name="weight")
        # 初始化偏执 0 形状是一维
        bias = tf.Variable(tf.constant(0.0, shape=[26]))
        # 预测None个样本的输出结果matrix（乘法） [None, 784]* [784, 10] + [10] = [None, 10]
        y_predict = tf.matmul(x, weight) + bias

    # 3、求出所有样本的损失，然后求平均值
    with tf.variable_scope("soft_cross"):

        # 求平均交叉熵损失
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_true, logits=y_predict))

    # 4、梯度下降求出损失
    with tf.variable_scope("optimizer"):
        train_op = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

    # 5、计算准确率
    with tf.variable_scope("acc"):
        equal_list = tf.equal(tf.argmax(y_true, 1), tf.argmax(y_predict, 1))

        # equal_list  None个样本   [1, 0, 1, 0, 1, 1,..........]
        accuracy = tf.reduce_mean(tf.cast(equal_list, tf.float32))

    # 定义一个初始化变量的op
    init_op = tf.global_variables_initializer()

    # 创建一个saver
    # saver = tf.train.Saver()

    # 开启会话去训练
    with tf.Session() as sess:
        # 初始化变量
        sess.run(init_op)

        # 建立events文件，然后写入
        filewriter = tf.summary.FileWriter("./test/", graph=sess.graph)
        # 定义一个合并变量de op
        merged = tf.summary.merge_all()
        # 迭代步数去训练，更新参数预测
        for i in range(2):

            # 取出真实存在的特征值和目标值
            mnist_x = x_train
            mnist_y = tf.one_hot(y_train,26)

            # 运行train_op训练
            sess.run(train_op, feed_dict={x: mnist_x, y_true: mnist_y})

            # 写入每步训练的值
            summary = sess.run(merged, feed_dict={x: mnist_x, y_true: mnist_y})

            # filewriter.add_summary(summary, i)

            print("训练第%d步,准确率为:%f" % (i, sess.run(accuracy, feed_dict={x: mnist_x, y_true: mnist_y})))

        # 保存模型
        # saver.save(sess, "./tmp/ckpt/fc_model")

    return None


full_connected()