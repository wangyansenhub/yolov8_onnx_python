import os
import random

trainval_percent = 0.2
train_percent = 0.8
txtfilepath = r'D:\\Tian\DB\\data\\change\\temp\\2\\xml'
total_xml = os.listdir(txtfilepath)
print(type(total_xml[1]))
num = len(total_xml)
list = range(num)
tv = int(num * trainval_percent)
tr = int(tv * train_percent)
trainval = random.sample(list, tv)

ftrainval = open(r'D:\\Tian\DB\\data\\valid.txt', 'w')
ftrain = open(r'D:\\Tian\DB\\data\\train.txt', 'w')


for i in range(0, num):

    total_xml[i] =total_xml[i].split('.')[0]
    name = "D:\\Tian\\DB\\data\\change\\temp\\2\\images\\" + total_xml[i] + ".tif"+ '\n'
    if i in trainval:
        ftrainval.write(name)
    else:
        ftrain.write(name)

ftrainval.close()
ftrain.close()
