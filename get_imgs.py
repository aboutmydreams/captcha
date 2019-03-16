from PIL import Image
from io import BytesIO
import os,requests,base64

url = 'http://210.35.251.243/reader/captcha.php'
for i in range(50):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save('imgs/{}.png'.format(str(i)))
    