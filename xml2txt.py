import xml.etree.ElementTree as ET
import math
import argparse
import os
'''
例：python xml2txt.py --xmlpath=E:\6394-05a-e3.xml   
'''
name_list = ['luosi']
def get_args():

    parse=argparse.ArgumentParser(description='命令行传入参数，文件路径')
    parse.add_argument('--xmlpath',default=None,type=str,help='xml文件路径')
    args=parse.parse_args()
    return args

def rotatePoint(xc, yc, xp, yp, theta):
    xoff = xp-xc
    yoff = yp-yc
    cosTheta = math.cos(theta)
    sinTheta = math.sin(theta)
    pResx = cosTheta * xoff + sinTheta * yoff
    pResy = - sinTheta * xoff + cosTheta * yoff
    return xc+pResx, yc+pResy

def getlabel(labelpath):
    root = ET.parse(labelpath).getroot()
    object_list = []
    for od in root.findall('size'):
        width = int(od.find('width').text)
        height = int(od.find('height').text)
    for ob in root.findall('object'):
        # name = int(ob.find('name').text)
        name = ob.find('name').text
        bndbox = ob.find('bndbox')
        robndbox = ob.find('robndbox')
        if bndbox:
            xmin = float(bndbox[0].text)
            ymin = float(bndbox[1].text)
            xmax = float(bndbox[2].text)
            ymax = float(bndbox[3].text)
            # ob_list = [name, int(xmin), int(ymin), int(xmax), int(ymin), int(xmax), int(ymax), int(xmin), int(ymax)]
            ob_list = [name, int(xmin), int(ymin), int(xmax), int(ymax)]

        else:
            cx = float(robndbox[0].text)
            cy = float(robndbox[1].text)
            w = float(robndbox[2].text)
            h = float(robndbox[3].text)
            angle = float(robndbox[4].text)
            x0, y0 = rotatePoint(cx, cy, cx-w/2, cy-h/2, -angle)
            x1, y1 = rotatePoint(cx, cy, cx+w/2, cy-h/2, -angle)
            x2, y2 = rotatePoint(cx, cy, cx+w/2, cy+h/2, -angle)
            x3, y3 = rotatePoint(cx, cy, cx-w/2, cy+h/2, -angle)
            ob_list = [name_list.index(name), int(x0)/width, int(y0)/height, int(x1)/width, int(y1)/height, int(x2)/width, int(y2)/height, int(x3)/width, int(y3)/height]
        object_list.append(ob_list)
    return object_list

def xml2txt(xml_path):
    object_list = getlabel(xml_path)
    f = open(xml_path[:-4]+'.txt', 'w')
    for ob in object_list:
        f.write('{},{},{},{},{}\n'.format(ob[0], ob[1], ob[2], ob[3], ob[4]))
      # f.write('{} {} {} {} {} {} {} {} {}\n'.format(
            # ob[0], ob[1], ob[2], ob[3], ob[4], ob[5], ob[6], ob[7], ob[8]))
        
        # f.close()

if __name__ == "__main__":
    args=get_args()
    xmlpath=r'./*.xml'
    import glob
    for i in glob.glob(xmlpath):
        print(i)
        xml2txt(i)
