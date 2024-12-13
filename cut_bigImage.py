import os
import math
from glob import glob
size=1024
step=1024
labelme_path=r'D:\Data\images\images\\'
if not os.path.exists(r'D:\Data\images\cut'):
    os.makedirs(r'D:\Data\images\cut')
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
CutList=[]
image_files = glob(labelme_path + "*.png")
for fileImag in image_files:
    try:
        print(fileImag)
        img = Image.open(fileImag)
        # try:
        name =fileImag.split('\\')[-1].split(".")[0]
        # except:
        # name = fileImag.split('/')[-1].split(".")[0]
        width, height = img.size
        for i in range(math.ceil(width / step)):
            for j in range(math.ceil(height / step)):
                x1 = i * step
                y1 = j * step
                x2 = size + i * step
                y2 = size + j * step
                if x2 > width:
                    x2 = width
                    x1 = width - size
                if y2 > height:
                    y2 = height
                    y1 = height - size
                cropped = img.crop((x1, y1, x2, y2))  # (left, upper, right, lower)
                extrema = cropped.convert("L").getextrema()
            
                if extrema != (0, 0):
                    cropped.save(r"D:\Data\images\cut\%s(%s_%s).jpg" % (name, x1, y1))
                    CutList.append('%s(%s_%s)'%(name, x1, y1))
    except:
        pass

