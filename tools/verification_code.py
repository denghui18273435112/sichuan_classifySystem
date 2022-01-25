import cv2 as cv
import pytesseract
from PIL import Image
from configs.path import data_path
import os
from configs.path import *
#
# def verification_code():
#     src = cv.imread(_file_path+os.sep+"code.png")
#     #cv.imshow('input image', src)
#     return recognize_text(src)
#     # cv.waitKey(0)
#     # cv.destroyAllWindows()
#
# def recognize_text(image):
#     # 边缘保留滤波  去噪
#     blur =cv.pyrMeanShiftFiltering(image, sp=8, sr=60)
#     #cv.imshow('dst', blur)
#     # 灰度图像
#     gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
#     # 二值化
#     ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
#     #print('二值化自适应阈值：{}'.format(ret))
#     #cv.imshow('binary', binary)
#     # 形态学操作  获取结构元素  开操作
#     kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 2))
#     bin1 = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
#     #cv.imshow('bin1', bin1)
#     kernel = cv.getStructuringElement(cv.MORPH_OPEN, (2, 3))
#     bin2 = cv.morphologyEx(bin1, cv.MORPH_OPEN, kernel)
#     #cv.imshow('bin2', bin2)
#     # 逻辑运算  让背景为白色  字体为黑  便于识别
#     cv.bitwise_not(bin2, bin2)
#     #cv.imshow('binary-image', bin2)
#     # 识别
#     test_message = Image.fromarray(bin2)
#     text = pytesseract.image_to_string(test_message)
#     return text
#     #print('识别结果：{}'.format(text))
#
# if __name__ == '__main__':
#     print(verification_code())

#----------------------------------------------------------------------------------------------------------------
# import cv2 as cv
# import pytesseract
# from PIL import Image
#
#
# def recognize_text(image):
#     # 边缘保留滤波  去噪
#     blur =cv.pyrMeanShiftFiltering(image, sp=8, sr=60)
#     cv.imshow('dst', blur)
#     # 灰度图像
#     gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
#     # 二值化
#     ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
#     print('二值化自适应阈值：{}'.format(ret))
#     cv.imshow('binary', binary)
#     # 形态学操作  获取结构元素  开操作
#     kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 2))
#     bin1 = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
#     cv.imshow('bin1', bin1)
#     kernel = cv.getStructuringElement(cv.MORPH_OPEN, (2, 3))
#     bin2 = cv.morphologyEx(bin1, cv.MORPH_OPEN, kernel)
#     cv.imshow('bin2', bin2)
#     # 逻辑运算  让背景为白色  字体为黑  便于识别
#     cv.bitwise_not(bin2, bin2)
#     cv.imshow('binary-image', bin2)
#     # 识别
#     test_message = Image.fromarray(bin2)
#     text = pytesseract.image_to_string(test_message)
#     print('识别结果：{}'.format(text))
#
# src = cv.imread(r'./1.png')
# #cv.imshow('input image', src)
# recognize_text(src)
# # cv.waitKey(0)
# # cv.destroyAllWindows()


import base64
import json
import requests
# 一、图片文字类型(默认 3 数英混合)：
# 1 : 纯数字
# 1001：纯数字2
# 2 : 纯英文
# 1002：纯英文2
# 3 : 数英混合
# 1003：数英混合2
#  4 : 闪动GIF
# 7 : 无感学习(独家)
# 11 : 计算题
# 1005:  快速计算题
# 16 : 汉字
# 32 : 通用文字识别(证件、单据)
# 66:  问答题
# 49 :recaptcha图片识别 参考 https://shimo.im/docs/RPGcTpxdVgkkdQdY
# 二、图片旋转角度类型：
# 29 :  旋转类型
#
# 三、图片坐标点选类型：
# 19 :  1个坐标
# 20 :  3个坐标
# 21 :  3 ~ 5个坐标
# 22 :  5 ~ 8个坐标
# 27 :  1 ~ 4个坐标
# 48 : 轨迹类型
#
# 四、缺口识别
# 18 : 缺口识别（需要2张图 一张目标图一张缺口图）
# 33 : 单缺口识别（返回X轴坐标 只需要1张图）
# 五、拼图识别
# 53：拼图识别
def base64_api(uname, pwd, img, typeid):
    with open(img, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""

def verification_code(name):
    #return base64_api(uname='denghui', pwd='dengHUI12', img=_file_path+os.sep+"code.png", typeid=3)
    return base64_api(uname='denghui', pwd='dengHUI12',
                      img=data_path+os.sep+name, typeid=3)
if __name__ == "__main__":
    print(verification_code())