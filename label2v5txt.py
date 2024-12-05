import os, glob
from PIL import Image

import argparse, json


def convert(size, box):
 
    dw = 1.0/size[0]
    dh = 1.0/size[1]
    x = (box[0]+box[1])/2.0
    y = (box[2]+box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

if __name__ == "__main__":
    image_path = r'./*.tif'
    class_list = ['coal', 'stone']
    import glob
    for image in glob.glob(image_path):
        name = image.split('\\')[-1].split('.')[0]
        label_txt = r'./\%s.txt'%name
        if os.path.exists(label_txt):
            f = open(label_txt, 'r')
            for data in f.readlines():
            
                data = data.split(',')
                label, x1, y1, x2, y2 = data[0], data[1], data[2], data[3], data[4]
                txt_name = name.split('/')[-1].split('.')
                label_path = '/'.join(name.split('/')[:-1])
                box = (int(x1), int(x2), int(y1), int(y2))
                img = Image.open(image)
                w, h = img.size
                cls_id = class_list.index(label)
                label_file = open(r'./%s.txt'%name, 'a')
                bb = convert((w,h), box)
                label_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        else:
            print(f"{name}  txt  is not exist")
            

