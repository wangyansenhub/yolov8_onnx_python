import json, glob, os

# JSON 字符串
# json_str
path = r'./json'
# 解析 JSON 字符串
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

for i in glob.glob(path + '/*.json'):
    with open(i, encoding='utf-8') as f:
        # data = json.load(f)

        name = i.split('\\')[-1].split('.')[0]
        data = json.load(f)

        # 获取 points, imageHeight, 和 imageWidth 的值
        # label = data['shapes'][0]['label']
        points = data['shapes'][0]['points']
        h = data['imageHeight']
        w = data['imageWidth']
        x1, y1, x2, y2 = int(points[0][0]), int(points[0][1]), int(points[1][0]), int(points[1][1])
        box = (int(x1), int(x2), int(y1), int(y2))
        cls_id = 7
        
        label_file = open(f"./{name}.txt", 'a')
        bb = convert((w,h), box)
        label_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
