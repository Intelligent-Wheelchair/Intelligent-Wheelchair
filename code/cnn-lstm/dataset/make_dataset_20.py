'''
Author: your name
Date: 2021-01-25 12:30:41
LastEditTime: 2021-01-25 13:05:04
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \modify_module\make_dataset.py
'''
import os

def generate(path):
    image_lists = os.listdir(path)#返回path下所有文件的列表
    print(image_lists)
    count=0
    context_list=[]
    with open(path +'\labels.txt', 'a+') as f:
        while True:
            if image_lists != []:
                del (image_lists[0])
            else:
                break
            label_list=[]
            for img_name in image_lists:
                #print(img_name)
                if img_name.split('_')[0] == 'F':
                    label = 1
                elif img_name.split('_')[0] == 'N':
                    label = 0
                label_list.append(label)
                #context = '{path}/{image_name},{label},'.format(path=path, image_name=img_name, label=label)
                context = '{path}/{image_name},'.format(path=path, image_name=img_name)
                context_list.append(context)
                count += 1
                if count % 20 == 0:
                    label_set=set(label_list)
                    temp1 = ""
                    for temp in context_list:
                        temp = str(temp)
                        temp1 += temp
                    if len(label_set)==1 and label == 1:
                        print("debug_label",label)
                    #context_list.append("\n")
                        context_str=temp1+'1'+'\n'
                    elif len(label_set)==1 and label==0:
                        context_str=temp1+"0"+"\n"
                    else:
                        context_list = []
                        break
                    # filename = os.path.split(file)[0]
                # filetype = os.path.split(file)[1]
                # print(filename, filetype)
                # if filetype == '.txt':
                #     continue
                # name = '/teeth' + '/' + file + ' ' + str(int(label)) + '\n'
                    print(context_str)
                    f.write(context_str)
                    context_list=[]
                    break
    print("finished!")


if __name__ == '__main__':
    # 看近处的物体为0 看远处的物体为1
    #img_path = r'D:\Program Files\Intelligent_Wheelchair\dataset\train'
    img_path = r'D:\Program Files\Intelligent_Wheelchair\dataset\test'
    #img_path = r'D:\Program Files\Intelligent_Wheelchair\dataset\val'
    generate(img_path)
