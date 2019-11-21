import xml.etree.ElementTree as ET
from os import getcwd
import os

classes = ['keys', 'aeroplane', 'bicycle','bird','boat','bottle','bus','car', 'cat', 'chair','cow','diningtable','dog','horse','motorbike','person', 'pottedplant','sheep',
'sofa','train','tvmonitor']

wd = getcwd()

def merge(txt1, txt2, txtOut):
    with open(txtOut, 'a') as output:
        for txt in (txt1, txt2):
            if(not os.path.exists(txt)):
                continue
            with open(txt) as f:
                output.write(f.read())
    return txtOut

def yoloCoordinate(size, box):
    '''dw = 1. / size[0]
    dh = 1. / size[1]'''

    # (xmin + xmax / 2)
    x = (box[0] + box[1]) // 2
    # (ymin + ymax / 2)
    y = (box[2] + box[3]) // 2

    # (xmax - xmin) = w
    w = box[1] - box[0]
    # (ymax - ymin) = h
    h = box[3] - box[2]

    '''x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (round(x,3), round(y,3), round(w,3), round(h,3))'''
    return (x, y, w, h)

def convert_annotation(dir, image_id):
    xml_file_name = image_id + ".xml"
    image_name = image_id + ".jpg"
    in_file = open(os.path.join(dir, 'Annotations', xml_file_name))

    tree = ET.parse(in_file)
    root = tree.getroot()
    xml_size = root.find('size')
    size = [int(xml_size.find("width").text), int(xml_size.find("height").text)]
    #print(size)
    img_path = os.path.join(dir, 'JPEGImages', image_name)
    line = img_path
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymin').text),
            int(xmlbox.find('ymax').text))
        (x, y, w, h) = yoloCoordinate(size, b)
        line += " {},{},{},{},{}".format(x, y, w, h, cls_id)
    line += "\n"
    return line

def main():
    dirs = (os.path.join(wd, "VOCdevkit","VOC2007"), os.path.join(wd, "VOCdevkit","VOC2012"))
    train_txt = 'trainval.txt'
    test_txt = 'test.txt'

    lines = []
    for folder in dirs:
        imgname_list = []
        merge_txt = os.path.basename(folder) + '.txt'
        merge_path = merge(os.path.join(folder, 'ImageSets', 'Main', train_txt), \
            os.path.join(folder, 'ImageSets', 'Main', test_txt), \
            os.path.join(wd, 'model_data', merge_txt))

        with open(merge_path) as f:
            all_lines = f.readlines()

        imgname_list = [c.strip() for c in all_lines]

        for image_id in imgname_list:
            lines.append(convert_annotation(folder, image_id))

    with open(os.path.join(wd, "VOCannotations.csv"), 'w') as csv_file:
        for line in lines:
            csv_file.write(line)

if __name__ == '__main__':
    main()