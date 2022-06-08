#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/05/26
"""
import cv2
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def main():
    # text_info = json.loads(open(dir_m2, 'r').readline())
    # font_color = text_info['color']
    # font_size = text_info['font_size']
    # content = text_info['content']
    font_type = './font/simsun.ttc'
    content = "咩咩咩"
    code = os.system(
        f"ffmpeg -y -threads {5} -i ./data/bkg.png "
        f"-vf 'drawtext=text={content}:expansion=normal:fontfile={font_type}:y={500}:x={1000}:fontcolor=black:fontsize=13' "
        f"-loglevel error ./data/bkgg.png")


# 返回指定路径图像的拉普拉斯算子边缘模糊程度值
def getImageVar(img_path):
    image = cv2.imread(img_path)
    img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
    return imageVar


# 返回给定文件夹下所有图片的路径列表
def listFolderImgPath(folder_img_path):
    img_path_list = []
    for filename in os.listdir(folder_img_path):
        filepath = os.path.join(folder_img_path, filename)
        img_path_list.append(filepath)
    return img_path_list


# 给单张图片添加文字(图片路径，文字)
def writeText(img_path, text):
    # 加载背景图片
    # img的类型是np.ndarray数组
    img = cv2.imread(img_path)
    # 在图片上添加文字信息
    # 颜色参数值可用颜色拾取器获取（(255,255,255)为纯白色）
    # 最后一个参数bottomLeftOrigin如果设置为True，那么添加的文字是上下颠倒的
    # img, text, org, fontFace, fontScale, color, thickness=None, lineType=None, bottomLeftOrigin=None
    composite_img = cv2.putText(img, text, (500, 1300), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                13, (0, 0, 0), 1, cv2.LINE_AA, False)
    cv2.imwrite("./data/t.png", composite_img)


def cv2ImgAddText(text_image, text, left, top, textColor, textSize):
    text_image = cv2.imread(text_image)
    text_image = Image.fromarray(cv2.cvtColor(text_image, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(text_image)
    # 字体的格式
    fontStyle = ImageFont.truetype("data/simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    cv2.imwrite("data/bkg.png", cv2.cvtColor(np.asarray(text_image), cv2.COLOR_RGB2BGR))


def cv2AddChineseText(img, text, position, textColor=(0, 255, 0), textSize=30):
    if isinstance(img, np.ndarray):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "./font/simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text(position, text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


if __name__ == '__main__':
    b = {"text": [{"top": 65, "font": "黑体", "left": 87, "color": "#000000", "width": 542, "height": 250,
                   "content": "今日小知识", "duration": 5, "font_size": 13, "layer_order": 2,
                   "is_animation": "false"},
                  {"top": 1252, "font": "黑体", "left": 70, "color": "#000000", "width": 922,
                   "height": 630, "content": "bbb", "duration": 5, "font_size": 13, "layer_order": 7,
                   "is_animation": "false"},
                  {"top": 610, "font": "黑体", "left": 72, "color": "#000000", "width": 922,
                   "height": 572, "content": "aaa", "duration": 5, "font_size": 13, "layer_order": 6,
                   "is_animation": "false"},
                  {"top": 437, "font": "黑体", "left": 70, "color": "#000000", "width": 930,
                   "height": 115, "content": "咩咩咩", "duration": 5, "font_size": 13, "layer_order": 5,
                   "is_animation": "false"}]}

    # a = "https://public-1255423687.cos.ap-shanghai.myqcloud.com/bg_import_1652363671114.jpg"
    # img = cv2.imread('./data/bkgg.png')
    # frame = cv2AddChineseText(img, "咩咩咩", (500, 1300), (0, 0, 0), 13)
    # cv2.imwrite('data/tt.png', frame)
    # writeText(img_path='./data/bkgg.png', text="咩咩咩")
    cv2ImgAddText(text_image='./data/30.png', text='咩咩咩', left=0, top=0, textColor=(0, 0, 0), textSize=15)
    # main()
    # os.system("ffmpeg -i ./data/bg.jpg -vf scale=30:30 ./data/30.png")
