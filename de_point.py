# 去除噪点
from PIL import Image,ImageDraw
from collections import Counter


# 二值数组
t2val = {}

# 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
# G: Integer 图像二值化阀值
# N: Integer 降噪率 0 <N <8
# Z: Integer 降噪次数
# 输出
#  0：降噪成功
#  1：降噪失败

def two_value(image, G):
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]):
            g = image.getpixel((x, y))
            if g > G:
                t2val[(x, y)] = 1
            else:
                t2val[(x, y)] = 0


def clear_noise(image, N, Z):
    # 0和1互相转换
    def one_zero(num):
        if num == 1:
            return 0
        else:
            return 1

    for i in range(0, Z):
        t2val[(0, 0)] = 1
        t2val[(image.size[0] - 1, image.size[1] - 1)] = 1

        for x in range(1, image.size[0] - 1):
            for y in range(1, image.size[1] - 1):
                L = t2val[(x, y)]# 0或1
                # 统计临近8个点是0还是1
                near8 = [t2val[(x - 1, y - 1)], t2val[(x - 1, y)],\
                t2val[(x - 1, y + 1)], t2val[(x, y - 1)], t2val[(x, y + 1)], \
                t2val[(x + 1, y - 1)], t2val[(x + 1, y)], t2val[(x + 1, y + 1)]]
                # data 计算0黑点数与 1白点数
                data = Counter(near8)
                if data[L] < N:
                    t2val[(x, y)] = one_zero(L)



def save_img(filename, size):
    image = Image.new("1", size)
    draw = ImageDraw.Draw(image)

    for x in range(0, size[0]):
        for y in range(0, size[1]):
            draw.point((x, y), t2val[(x, y)])

    image.save(filename)

for i in range(1,50):
    path =  'imgs/' + str(i) + ".png"
    image = Image.open(path).convert("L")
    two_value(image, 100)
    clear_noise(image, 2, 1)
    path1 = 'de_point_imgs/' + str(i) + ".jpeg"
    save_img(path1, image.size)


