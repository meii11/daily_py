#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/13
"""
import os

import cv2
import numpy as np


def main():
    """
    {"top": 420, "url": "https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655117797854",
         "crop": {"top": -21, "left": 167, "width": 80, "height": 96}, "left": 87, "text": {}, "width": 250, "height": 300, "duration": 5, "layer_order": 6},
    {"top": 622, "url": "https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655117807149", "crop": {"top": 272, "left": 550, "width": 374, "height": 449},
         "left": 467, "text": {}, "width": 250, "height": 300, "duration": 5, "layer_order": 1}
    """
    img = '../data/budala.png'
    w_bkg = '../data/white_bkg_1080_1920.jpg'
    # alpha_img = np.full(())

    # 925 * 520
    crop_size = {'top': -21, 'left': 167, 'width': 80, 'height': 96}
    img_width = 250
    img_height = 300
    # c_height = crop_size['top'] + crop_size['height'] if crop_size['top'] > 0 else -crop_size['top'] + crop_size[
    #     'height']
    # c_width = crop_size['left'] + crop_size['width'] if crop_size['left'] > 0 else -crop_size['left'] + crop_size[
    #     'width']
    alpha_img = np.full((crop_size['height'], crop_size['width'], 4), 255)
    cv2.imwrite('../data/alpha.png', alpha_img)
    alpha_img = '../data/alpha.png'
    new_c_height = min(crop_size['height'] if crop_size['top'] > 0 else crop_size['top'] + crop_size['height'],
                       img_height)
    new_c_width = min(crop_size['width'] if crop_size['left'] > 0 else crop_size['left'] + crop_size['width'],
                      img_width)
    new_top = -crop_size['top'] if crop_size['top'] < 0 else 0
    new_left = -crop_size['left'] if crop_size['left'] < 0 else 0

    # crop img
    resize_img = '../data/crop_dog.png'
    os.system(f"ffmpeg -y -i {img} -vf crop=w={new_c_width}:h={new_c_height}:x={new_left}:y={new_top} {resize_img}")

    # overlay
    os.system(
        f"ffmpeg -y -i {alpha_img} -i {resize_img} -filter_complex 'overlay={new_left}:{new_top}' -loglevel error ../data/crop_dog_f.png")

    # overlay on bkg
    os.system(
        f"ffmpeg -y -i {w_bkg} -i ../data/crop_dog_f.png -filter_complex 'overlay={new_left}:{new_top}' -loglevel error ../data/crop_dog_ff.png")

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
    # main()
    positive_coo()
    # d = {'
    # fps': 30, 'stories': [
    #     {'fps': 30,
    #      'order': 1,
    #      'lay_out': {
    #          'text': [],
    #          'charts': [],
    #          'images': [
    #              {'top': 0, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/bg_import_1652339586034.jpg',
    #               'crop': {}, 'left': 0, 'text': {}, 'width': 1080, 'height': 1920, 'duration': 30, 'layer_order': 0},
    #              {'top': 0, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655084473339',
    #               'crop': {'top': 114, 'left': -49, 'width': 1018, 'height': 326}, 'left': 0, 'text': {}, 'width': 1075,
    #               'height': 345, 'duration': 5, 'layer_order': 10}],
    #          'videos': [], 'persons': [{'id': '007red', 'top': 27,
    #                                     'crop': {'top': 0, 'left': 0, 'width': 768, 'circle': 'false', 'height': 768},
    #                                     'left': 745, 'text': {'content': '负值crop坐标'}, 'audio': 's019', 'speed': 1,
    #                                     'width': 277, 'height': 277, 'duration': 5, 'layer_order': 14}]},
    #      'batch_no': '985848103393296384'}], 'batch_no': '985848103393296384', 'resolution': '1080*1920',
    #      'video_type': 'mp4', 'time_now': '10_0_15',
    #      'base': '/data/caopei/1-code/BackgroungCombination_chopei/local/985848103393296384'}

    d = {"fps": 30, "stories": [{"fps": 30, "order": 1, "lay_out": {"text": [], "charts": [], "images": [
        {"top": 0, "url": "https://public-1255423687.cos.ap-shanghai.myqcloud.com/bg_import_1652339586034.jpg",
         "crop": {}, "left": 0, "text": {}, "width": 1080, "height": 1920, "duration": 30, "layer_order": 0},
        {"top": 420, "url": "https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655117797854",
         "crop": {"top": -21, "left": 167, "width": 80, "height": 96}, "left": 87, "text": {}, "width": 250,
         "height": 300, "duration": 5, "layer_order": 6},
        {"top": 622, "url": "https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655117807149",
         "crop": {"top": 272, "left": 550, "width": 374, "height": 449},
         "left": 467, "text": {}, "width": 250, "height": 300, "duration": 5, "layer_order": 1}],

                                                                    "videos": [], "persons": [
            {"id": "007red", "top": 50,
             "crop": {"top": 114, "left": 111, "width": 577, "circle": "false", "height": 811}, "left": 787,
             "text": {"content": "测试负值，回显"}, "audio": "s019", "speed": 1, "width": 240, "height": 337, "duration": 5,
             "layer_order": 4}]}, "batch_no": "985983935953502208"}], "batch_no": "985983935953502208",
         "resolution": "1080*1920", "video_type": "mp4"}
