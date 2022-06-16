#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/15
"""
import ffmpeg
import numpy as np
import os


class cal_negative_coo:
    def preprocess(self, material_dir, crop_coo, full_coo, output_dir):
        # 先支持图像版本，假设图片是文件格式，后序应该需要支持numpy格式才能加速，需要have a try
        m_info = ffmpeg.probe(material_dir)['streams'][0]
        img_width, img_height = m_info['width'], m_info['height']

        if crop_coo['left'] < 0 and crop_coo['top'] >= 0:
            c_left = 0
            c_top = crop_coo['top']

            c_height = min(crop_coo['height'], img_height - crop_coo['top'])
            c_width = min(crop_coo['width'] + crop_coo['left'], img_width)

            f_top = full_coo['top']
            f_left = full_coo['left'] - crop_coo['left']

            resize_width = c_width * full_coo['width'] // crop_coo['width']
            resize_height = c_height * full_coo['height'] // crop_coo['height']
        # situation 2: left>0 top<0
        elif crop_coo['left'] >= 0 and crop_coo['top'] < 0:
            c_top = 0
            c_left = crop_coo['left']

            c_height = min(crop_coo['height'] + crop_coo['top'], img_height)
            c_width = min(img_width - crop_coo['left'], crop_coo['width'])

            f_top = full_coo['top'] - crop_coo['top']
            f_left = full_coo['left']

            resize_width = c_width * full_coo['width'] // crop_coo['width']
            resize_height = c_height * full_coo['height'] // crop_coo['height']

        # situation 3: left<0 top<0
        elif crop_coo['left'] < 0 and crop_coo['top'] < 0:
            c_top = 0
            c_left = 0

            c_height = min(crop_coo['height'] + crop_coo['top'], img_height)
            c_width = min(crop_coo['width'] + crop_coo['left'], img_width)

            f_top = full_coo['top'] - crop_coo['top']
            f_left = full_coo['left'] - crop_coo['left']

            resize_width = c_width * full_coo['width'] // crop_coo['width']
            resize_height = c_height * full_coo['height'] // crop_coo['height']
        # situation 4: all > 0
        else:
            c_left = crop_coo['left']
            c_top = crop_coo['top']

            c_height = min(crop_coo['height'], img_height-crop_coo['top'])
            c_width = min(crop_coo['width'], img_width-crop_coo['left'])

            resize_width = c_width * full_coo['width'] // crop_coo['width']
            resize_height = c_height * full_coo['height'] // crop_coo['height']

        # step1 crop material
        resize_material = './doggy' + '_resize' + os.path.splitext(material_dir)[1]
        os.system(
            f"ffmpeg -y -i {material_dir} -vf crop=w={c_width}:h={c_height}:x={c_left}:y={c_top} -loglevel error {resize_material}")

        os.system(
            f"ffmpeg -y -i {resize_material} -vf scale={resize_width}:{resize_height} -loglevel error {output_dir}")
        pass


def main():
    cal = cal_negative_coo()
    image_dir = 'saber.jpg'
    crop_coo = {'top': -603, 'left': 0, 'width': 1924, 'height': 2309}
    full_coo = {'top': 420, 'left': 87, 'width': 250, 'height': 300}

    output_dir = './saber123.png'
    cal.preprocess(image_dir, crop_coo, full_coo, output_dir)


if __name__ == '__main__':
    main()
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
