from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random,time



# 随机字母:
def rndChar():
    return chr(random.randint(65, 90))

# 随机颜色1:
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

# 240 x 60:
# width = 60 * 4
# height = 60

def make_captcha(width,height,num_of_str,gray_value=255):
    image = Image.new('RGB', (width, height), (255, 255, 255))

    # 创建Font对象:
    font = ImageFont.truetype('ヒラギノ角ゴシック W8.ttc', 31) # '/Library/Fonts/Bodoni 72.ttc'

    # 创建Draw对象:
    draw = ImageDraw.Draw(image)

    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            # draw.point((x, y), fill=rndColor())
            draw.point((x, y), fill=(255,255,255))

    # 输出文字:
    char_list = [rndChar() for i in range(num_of_str)]

    for t in range(num_of_str):
        # rndColor2()
        draw.text((height * t, 1), char_list[t], font=font, fill=(0,0,0))

    # 模糊:
    # image = image.filter(ImageFilter.BLUR)
    # image.save('train_imgs/1.png', 'jpeg');
    return char_list,image



def get_modes(img):
    img = img.convert('L')
    mode = np.array(img)
    mode = np.where(mode < 100, 0, 1)
    return mode

def mode_to_img(mode,background=None):
    if background:
        mode = np.where(mode < 1, 0, background)
    array_mode = np.array(mode).astype('uint8')
    image = Image.fromarray(array_mode).convert('RGB')
    return image


# 随机增加临近噪点

    
# 随机造成缺失

# 偏移

# 生成训练集图片
for i in range(1):
    char_list,image = make_captcha(30,32,num_of_str=1,gray_value=255)
    file_name = char_list[0] + '-' + str(int(time.time()))[-8:]
    image.show()
    # 在这里增加难度与异动
    mode = get_modes(image)


    # image.save('train_imgs/{}.png'.format(file_name))
    image.show()