#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/20
"""
import os

import cv2
import numpy as np
import cv2
from matplotlib import pyplot as plt
import glob as gb


def _draw_circle11(frame_input):
    frame = cv2.imread(frame_input)
    height, width = frame.shape[:2]

    b_channel, g_channel, r_channel = cv2.split(frame)
    alpha_channel = np.full(b_channel.shape, 255.0)

    circle_mask = cv2.imread("./circle_data/circle_mask.png")
    # assert self.crop['width'] == self.crop['height'], "圆参数不正确！请检查"
    circle_mask = cv2.resize(circle_mask, (500, 500))
    c_mask = circle_mask >= 200.0

    c_alpha = np.array(c_mask[:, :, 0] * alpha_channel, dtype=b_channel.dtype)
    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, c_alpha))
    cv2.imwrite("ccc.png", img_BGRA)


def draw_circle():
    # os.system('ffmpeg -i circle_data/bkg.jpg -vf crop=500:500:0:0 circle_data/bkg_square.jpg')
    # img = cv2.imread("circle_data/bkg_square.jpg")
    # # 对读取的图片进行画圆，并保存到last_img
    # last_img = cv2.circle(img, center=(250, 250), radius=250, color=(255, 0, 3), thickness=6)
    # # 显示图片
    # # cv2.imshow('for  circle', last_img)
    # # 保存图片
    # cv2.imwrite('./test1.jpg', last_img)
    # # cv2.waitKey(0)
    # # cv2.destroyAllWindows()
    os.system("ffmpeg -y -i circle_data/qiyu.png -vf scale=500:500 circle_data/qiyu_square.png")
    # os.system(
    #     "ffmpeg -y -i circle_data/qiyu_square.png -i circle_data/bkg_square.jpg.png "
    #     "-filter_complex '[0]scale=500:500[ava];[1]alphaextract[alfa];[ava][alfa]alphamerge' circle_ava.png")
    # # os.system("ffmpeg -i avatar.png -i mask.png -filter_complex "[0]scale=400:400[ava];[1]alphaextract[alfa];[ava][alfa]alphamerge" output.png")
    os.system("ffmpeg -y -i circle_data/qiyu_square.png -i circle_data/bkg_square.jpg.png "
              "-filter_complex 'overlay=0:0' -loglevel error circle_ava.png")


# 图像处理，获取图片最大内接圆，其他区域置为透明
def img_deal(input_img):
    # cv2.IMREAD_COLOR，读取BGR通道数值，即彩色通道，该参数为函数默认值
    # cv2.IMREAD_UNCHANGED，读取透明（alpha）通道数值
    # cv2.IMREAD_ANYDEPTH，读取灰色图，返回矩阵是两维的
    img = cv2.imread(input_img, cv2.IMREAD_UNCHANGED)
    rows, cols, channel = img.shape

    # 创建一张4通道的新图片，包含透明通道，初始化是透明的
    img_new = np.zeros((rows, cols, 4), np.uint8)
    img_new[:, :, 0:3] = img[:, :, 0:3]

    # 创建一张单通道的图片，设置最大内接圆为不透明，注意圆心的坐标设置，cols是x坐标，rows是y坐标
    img_circle = np.zeros((rows, cols, 1), np.uint8)
    img_circle[:, :, :] = 0  # 设置为全透明
    img_circle = cv2.circle(img_circle, (cols // 2, rows // 2), min(rows, cols) // 2, (255), -1)  # 设置最大内接圆为不透明

    # 图片融合
    img_new[:, :, 3] = img_circle[:, :, 0]

    # 保存图片
    cv2.imwrite(input_img + ".png", img_new)
    # cv2.imencode('.jpg', img)[1].tofile('./9.jpg')  # 保存到另外的位置

    # 显示图片，调用opencv展示
    # cv2.imshow("img_new", img_new)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 显示图片，调用matplotlib.pyplot展示
    plt.subplot(121), plt.imshow(img_convert(img), cmap='gray'), plt.title('IMG')
    plt.subplot(122), plt.imshow(img_convert(img_new), cmap='gray'), plt.title('IMG_NEW')
    plt.show()


# cv2与matplotlib的图像转换，cv2是bgr格式，matplotlib是rgb格式
def img_convert(cv2_img):
    # 灰度图片直接返回
    if len(cv2_img.shape) == 2:
        return cv2_img
    # 3通道的BGR图片
    elif len(cv2_img.shape) == 3 and cv2_img.shape[2] == 3:
        b, g, r = cv2.split(cv2_img)
        return cv2.merge((r, g, b))
    # 4通道的BGR图片
    elif len(cv2_img.shape) == 3 and cv2_img.shape[2] == 4:
        b, g, r, a = cv2.split(cv2_img)
        return cv2.merge((r, g, b, a))
    # 未知图片格式
    else:
        return cv2_img


class Cir:
    def preprocess(self):
        bkg_img = './circle_data/bkg_500.png'
        # 裁剪成正方形
        # os.system("ffmpeg -y -i ./circle_data/bkg.jpg -vf crop=3000:3000:0:0 ./circle_data/bkg_square.png")
        # 缩小
        # os.system("ffmpeg -y -i ./circle_data/bkg_square.png -vf scale=500:500 ./circle_data/bkg_500.png")
        target_img = './circle_data/qiyu_500.png'

        # step1 需要将target和背景套出圆形
        # self._to_circle(target_img)

        # step2 拼起来
        self._concat(bkg='ccc.png', target='ccc1.png')

    def _to_circle(self, img):
        img_info = cv2.imread(img, cv2.IMREAD_UNCHANGED)
        height, width = img_info.shape[:2]

        b_channel, g_channel, r_channel, alpha_channel = cv2.split(img_info)
        # alpha_channel = np.full(b_channel.shape, 255.0)

        circle_mask = cv2.imread("./circle_data/circle_mask.png")
        # assert self.crop['width'] == self.crop['height'], "圆参数不正确！请检查"
        circle_mask = cv2.resize(circle_mask, (height, width))
        c_mask = circle_mask >= 200.0

        c_alpha = np.array(c_mask[:, :, 0] * alpha_channel, dtype=b_channel.dtype)
        img_BGRA = cv2.merge((b_channel, g_channel, r_channel, c_alpha))
        cv2.imwrite("ccc1.png", img_BGRA)

    def _concat(self, bkg, target):
        # os.system(f"ffmpeg -i {bkg} -i {target} -filter_complex overlay=0:0 final.png")
        # os.system(f"ffmpeg -i 123.jpg -i final.png -filter_complex overlay=0:0 final1.png")
        os.system("ffmpeg -y -i final1.png -vf crop=600:600:0:0 final12.png")
def main():
    # target_size = [500, 500]
    # draw_circle()
    # img_deal('./circle_data/bkg_square.jpg')
    _draw_circle11('./circle_data/qiyu_square.png')


if __name__ == '__main__':
    Cir().preprocess()
