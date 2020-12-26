import os
import sys
import h5py
from PIL import Image

def convert(size, box):
  dw = size[0]
  dh = size[1]
  x = box[0] + (box[2] / 2.0)
  y = box[1] + (box[3] / 2.0)
  w = box[2]
  h = box[3]
  x = x/dw
  w = w/dw
  y = y/dh
  h = h/dh
  return (x,y,w,h)

def loadSvhn(subdir):
    dir = 'data/' + subdir
    print('process folder : %s' % dir)
    filenames = []
    #dir = os.path.join(svhnPath, path)
    for filename in os.listdir(dir):
        filenameParts = os.path.splitext(filename)
        if filenameParts[1] != '.png':
            continue
        filenames.append(filenameParts)
    filenames.sort(key=lambda tup: int(tup[0]))
    svhnMat = h5py.File(name=os.path.join(dir, 'digitStruct.mat'), mode='r')
    datasets = []
    filecounts = len(filenames)
    for idx, file in enumerate(filenames):
        boxes = {}
        filenameNum = file[0]
        item = svhnMat['digitStruct']['bbox'][int(filenameNum) - 1].item()
        for key in ['label', 'left', 'top', 'width', 'height']:
            attr = svhnMat[item][key]
            values = [svhnMat[attr.value[i].item()].value[0][0]
                      for i in range(len(attr))] if len(attr) > 1 else [attr.value[0][0]]
            boxes[key] = values
        datasets.append({'dir': dir, 'file': file, 'boxes': boxes})
        if idx % 1000 == 0: print('-- loading %d / %d' % (idx, filecounts))
    return datasets

if __name__ == '__main__':
    for sub_dir in ['train', 'val']:
        data_sets = loadSvhn(sub_dir)
        txt = 'data/' + sub_dir + '.txt'
        train_val_txt = open(txt,mode='w',encoding='utf-8')
        # data_sets = [{'dir': './', 'file': ('01', '.png'),
        #              'boxes': {'label': ['0'], 'left': [12], 'top': [10], 'width': [20], 'height': [30]}}]
        print('Processing locations to txt file ...')
        for ds in data_sets:
            txt_file = os.path.join(ds['dir'], ds['file'][0] + '.txt')
            boxes = ds['boxes']
            labels = boxes['label']
            img_path = os.path.join(ds['dir'], ds['file'][0] + '.png')
            im=Image.open(img_path)
            w= int(im.size[0])
            h= int(im.size[1])
            train_val_txt.write(img_path + '\n')
            lines = []
            with open(txt_file, mode='w', encoding='utf-8') as fs:
                for i in range(len(labels)):
                    label = boxes['label'][i]
                    left = boxes['left'][i]
                    top = boxes['top'][i]
                    width = boxes['width'][i]
                    height = boxes['height'][i]
                    b = (float(left), float(top), float(width), float(height))
                    bb = convert((w,h), b)
                    lines.append(str(int(label))+' '+str(bb[0])+' '+str(bb[1])+' '+str(bb[2])+' '+str(bb[3]))
                    #lines.append('%s,%s,%s,%s,%s' % (int(label), left, top, width, height))
                fs.write('\n'.join(lines))
        print('Done!')
        train_val_txt.close()
    
        fd=open(txt,"r")
        d=fd.read()
        fd.close()
        m=d.split("\n")
        s="\n".join(m[:-1])
        fd=open(txt,"w+")
        for i in range(len(s)):
            fd.write(s[i])
        fd.close()
