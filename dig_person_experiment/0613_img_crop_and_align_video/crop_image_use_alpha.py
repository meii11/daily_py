#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/13
"""
import os

import cv2
import numpy as np
import math

def main(crop_size):
    """
    {"top": 420, "url": "https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655117797854",
         "crop": {"top": -21, "left": 167, "width": 80, "height": 96}, "left": 87, "text": {}, "width": 250, "height": 300, "duration": 5, "layer_order": 6},
    {"top": 622, "url": "https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655117807149", "crop": {"top": 272, "left": 550, "width": 374, "height": 449},
         "left": 467, "text": {}, "width": 250, "height": 300, "duration": 5, "layer_order": 1}
    """
    img = '../data/new_dog.png'
    w_bkg = '../data/white_bkg_1080_1920.jpg'
    # alpha_img = np.full(())
    img_info = cv2.imread(img).shape[:2]
    img_width = img_info[1]
    img_height = img_info[0]


    # crop_info_cal
    # 925 * 520
    # crop_size = {"top": -202, "left": 512, "width": 412, "height": 495}

    # 三种情况计算crop的top\left\height\width
    # situation 1: left<0 top>0
    if crop_size['left'] < 0 and crop_size['top'] >= 0:
        c_left = 0
        c_top = crop_size['top']

        c_height = min(crop_size['height'], img_height-crop_size['top'])
        c_width = min(crop_size['width']+crop_size['left'], img_width)

        new_crop_top = 0
        new_crop_left = -crop_size['left']
    # situation 2: left>0 top<0
    elif crop_size['left'] >= 0 and crop_size['top'] < 0:
        c_top = 0
        c_left = crop_size['left']

        c_heigth = min(crop_size['height']+crop_size['top'], img_height)
        c_width = min(img_width-crop_size['left'], crop_size['width'])

        new_crop_top = -crop_size['top']
        new_crop_left = 0
    # situation 2: left<0 top<0
    elif crop_size['left'] < 0 and crop_size['top'] < 0:
        c_top = 0
        c_left = 0

        c_heigth = min(crop_size['height']+crop_size['top'], img_height)
        c_width = min(crop_size['width']+crop_size['left'], img_width)

        new_crop_top = -crop_size['top']
        new_crop_left = -crop_size['left']
    else:
        pass
    alpha_img = np.full((crop_size['height'], crop_size['width'], 4), 255)
    cv2.imwrite('../data/alpha.png', alpha_img)
    alpha_img = '../data/alpha.png'

    # crop img
    resize_img = '../data/crop_dog.png'
    os.system(f"ffmpeg -y -i {img} -vf crop=w={c_width}:h={c_heigth}:x={c_left}:y={c_top} {resize_img}")

    # overlay
    os.system(
        f"ffmpeg -y -i {alpha_img} -i {resize_img} -filter_complex 'overlay={new_crop_left}:{new_crop_top}' -loglevel error ../data/crop_dog_f.png")

    # overlay on bkg
    # os.system(
    #     f"ffmpeg -y -i {w_bkg} -i ../data/crop_dog_f.png -filter_complex 'overlay={467}:{622}' -loglevel error ../data/crop_dog_ff.png")

    # code = os.system(
    #     f"ffmpeg -y -threads {t_num} -i {dir_m1} -i {dir_m2} "
    #     f"-filter_complex 'overlay={left_m2}:{top_m2}' -loglevel error {mid_dir}")
    pass


def positive_coo():
    img = '../data/new_dog.png'
    w_bkg = '../data/white_bkg_1080_1920.jpg'
    # {"top": 622, "url": "https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655117807149",
    #  "crop": {"top": 272, "left": 550, "width": 374, "height": 449},
    #  "left": 467, "text": {}, "width": 250, "height": 300, "duration": 5, "layer_order": 1}
    crop_size = {"top": 272, "left": 550, "width": 374, "height": 449}
    height = 300
    width = 250

    alpha_img = np.full((crop_size['height'], crop_size['width'], 4), 255)
    cv2.imwrite('../data/alpha.png', alpha_img)

    c_img = cv2.imread(img)
    image = c_img[crop_size['top']:crop_size['top'] + crop_size['height'],
            crop_size['left']:crop_size['left'] + crop_size['width']]

    resize_img = '../data/resize_dog.png'
    cv2.imwrite(resize_img, image)
    os.system(
        f"ffmpeg -y -i {tmp_img} -vf scale={resize[0]}:{resize[1]} -loglevel error {resize_img}")
    os.system(
        f"ffmpeg -y -i {w_bkg} -i {resize_img} -filter_complex 'overlay=0:0' -loglevel error ../data/crop_dog_ff.png")


if __name__ == '__main__':
    # os.system('rm -f 1 2')
    main({'top': -202, 'left': 560, 'width': 365, 'height': 469})
# {'fps': 30, 'stories': [{'fps': 30, 'order': 1, 'lay_out': {'text': [], 'charts': [], 'images': [
#     {'top': 0, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/bg_import_1652339586034.jpg', 'crop': {},
#      'left': 0, 'text': {}, 'width': 1080, 'height': 1920, 'duration': 30, 'layer_order': 0},
#     {'top': 670, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655191394318',
#      'crop': {'top': 143, 'left': 0, 'width': 391, 'height': 579}, 'left': 58, 'text': {}, 'width': 260, 'height': 385,
#      'duration': 5, 'layer_order': 7},
#     {'top': 120, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655191370657',
#      'crop': {'top': -202, 'left': 560, 'width': 365, 'height': 469}, 'left': 535, 'text': {}, 'width': 315,
#      'height': 405, 'duration': 5, 'layer_order': 5},
#     {'top': 1208, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655191413628',
#      'crop': {'top': 26, 'left': 173, 'width': 533, 'height': 435}, 'left': 68, 'text': {}, 'width': 463, 'height': 378,
#      'duration': 5, 'layer_order': 8},
#     {'top': 130, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655191367412',
#      'crop': {'top': -202, 'left': 0, 'width': 574, 'height': 485}, 'left': 55, 'text': {}, 'width': 355, 'height': 300,
#      'duration': 5, 'layer_order': 1},
#     {'top': 655, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655191405433',
#      'crop': {'top': 322, 'left': 380, 'width': 545, 'height': 332}, 'left': 533, 'text': {}, 'width': 493,
#      'height': 300, 'duration': 5, 'layer_order': 6}], 'videos': [], 'persons': [
#     {'id': '007red', 'top': 1408, 'crop': {'top': 114, 'left': 111, 'width': 577, 'circle': 'false', 'height': 811},
#      'left': 715, 'text': {'content': '裁剪的5种情况'}, 'audio': 's019', 'speed': 1, 'width': 365, 'height': 513,
#      'duration': 5, 'layer_order': 4}]}, 'batch_no': '986292547422781440'}], 'batch_no': '986292547422781440',
#  'resolution': '1080*1920', 'video_type': 'mp4', 'time_now': '15_27_5',
#  'base': '/data/caopei/1-code/BackgroungCombination_chopei/local/986292547422781440'}