# --------------------------------------------------------------------------
# 将label中标注的json文件，转化为可用于分割训练的标签二值化黑白png图片
# -------------------------------------------------------------------------
import os
import cv2
import numpy as np
import shutil
import glob
import re
import xlwt
from skimage.morphology import thin, skeletonize
from skimage import io
import matplotlib.pyplot as plt


# def json_png():  第一次转换用到
path = r'datasets'  # 这里是指.json文件所在文件夹的路径
# 批量转换，修改此路径
# 此路径为，json文件所在路径
# def extract_png():  第二次转换用到
path_before = os.path.join(path, "before")
path_save_png = os.path.join(path, "json_png")  # 将标签图从json文件中批量取出后指定保存的文件目录
path_save_png_binary = os.path.join(path, "json_png_binary")  # 二至图像最终保存的路径
path_save_png_01binary = os.path.join(path, "json_png_01binary")
path_save_png_thin = os.path.join(path, "json_png_thin")
path_save_png_skel = os.path.join(path, "json_png_skel")


def pre_treatment():
    '''
    创建三个文件夹用于存储
    json_data用于存储json转换img.png     label.png    label_names.txt   label_viz.png的文件夹
    json_png用于存储从json_data提取出来的label。png（最终存储名字与json文件对应）
    json_png_binary 用于存储最终转换后的8位的单通道黑白图像
    :return:
    '''
    if os.path.isdir(os.path.join(path, "json_png")) is False:
        os.mkdir(os.path.join(path, "json_png"))
    else:
        print('文件已存在')

    if os.path.isdir(os.path.join(path, "json_png_binary")) is False:
        os.mkdir(os.path.join(path, "json_png_binary"))
    else:
        print('文件已存在')

    if os.path.isdir(os.path.join(path, "json_png_01binary")) is False:
        os.mkdir(os.path.join(path, "json_png_01binary"))
    else:
        print('文件已存在')

    if os.path.isdir(os.path.join(path, "json_png_thin")) is False:
        os.mkdir(os.path.join(path, "json_png_thin"))
    else:
        print('文件已存在')

    if os.path.isdir(os.path.join(path, "json_png_skel")) is False:
        os.mkdir(os.path.join(path, "json_png_skel"))
    else:
        print('文件已存在')


def json_png():
    '''
    批量将json转换为img.png     label.png    label_names.txt   label_viz.png
    并存储至当前文件夹下的json_date文件夹中
    :return: 无
    '''
    json_file = glob.glob(os.path.join(path_before, "*.json"))  # 找出before目录所有带.json的文件
    os.system("activate labelme")  # 激活labelme环境（根据自己设置的修改）
    for file in json_file:
        os.system("labelme_json_to_dataset.exe %s" % (file))  # 调用进行批量转换

def extract_png():
    '''
    将标签图从json_data文件中批量取出
    :return:
    '''
    for eachfile in os.listdir(path_before):
        path1 = os.path.join(path_before, eachfile)  # 获取单个json文件夹的目录
        if os.path.isdir(path1):
            if path1.find("_json") > 0:  # 判断path1路径是否存在
                if os.path.exists(path1 + '/label.png'):  # 判断path1路径下label.png是否存在
                    path2 = os.path.join(path1, 'label.png')  # 获取PNG所在的路径，准备等待复制
                    path_save = os.path.join(path_save_png, (eachfile.split('_json')[0] + '.png'))  # 将png复制到path2路径下的文件夹中去
                    shutil.copy(path2, path_save)  # 将path2文件复制到path_save
                    print(path2 +"   " + path_save)
                    print(eachfile + ' successfully moved')


def png_to_binary():
    '''
    由于数据集是做二分类分割，所以，需要将ground_truth转换为8位的单通道黑白图像和1位的单通道黑白图像，才能作为训练时的label使用。
    将提取出来的png转换为8位的单通道黑白图像和1位的单通道黑白图像
    '''
    for im in os.listdir(path_save_png):
        img = cv2.imread(os.path.join(path_save_png, im))
        b, g, r = cv2.split(img)
        r[np.where(r != 0)] = 255 # 转为黑白二值图，如果不是做二分类需要修改下面的代码
        cv2.imwrite(os.path.join(path_save_png_binary, im), r) # 保存为单通道二值图
        cv2.destroyAllWindows()
        r[np.where(r != 0)] = 1
        cv2.imwrite(os.path.join(path_save_png_01binary, '01' + im), r)
        cv2.destroyAllWindows()

        # 多分类的代码，没有验证过，不一定对
        # img = cv2.imread(os.path.join(path_save_png, im))
        # cv2.imwrite(os.path.join(path_save_png_binary, im)) # 保存为单通道二值图
        # cv2.destroyAllWindows()


def png_refine():
    '''
    采用skimage 模块的 skeletonize和 thin 方法对二值图像做细化处理
    :return:
    '''
    path_save_subplot = os.path.join(path, "subplot")
    for im in os.listdir(path_save_png_01binary):
        img = cv2.imread(os.path.join(path_save_png_01binary, im),0)
        thinned = thin(img)
        skel = skeletonize(img)
        io.imsave(os.path.join(path_save_png_thin, 'thin' + im), thinned)
        io.imsave(os.path.join(path_save_png_skel, 'skel' + im), skel)
        f, ax = plt.subplots(2, 2)
        ax[0, 0].imshow(img)
        ax[0, 0].set_title('original')
        ax[0, 0].get_xaxis().set_visible(False)
        ax[0, 1].axis('off')
        ax[1, 0].imshow(thinned)
        ax[1, 0].set_title('thin')
        ax[1, 1].imshow(skel)
        ax[1, 1].set_title('skeletonize')
        plt.savefig(os.path.join(path_save_subplot, im))
        plt.close()


def process():
    #pre_treatment()  # 预处理，创建存储所需的相应文件夹
    #json_png()  # 调用labelme的json转换png程序
    #extract_png()  # 从转换的数据中提取png图像
    png_to_binary()  # 将png转换为8位的单通道黑白图像，用于分割训练
    png_refine()



if __name__ == "__main__":
    process()
