#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/01
"""
import os
import requests
import time


def main():
    # os.system("ffmpeg -y -i ./data/bg.jpg -vf scale=1080:1920 ./new_bg.png")
    os.system("ffmpeg -y -i ./data/bg.jpg -i ./data/qianxi.mp4 -filter_complex 'overlay=55:977' ./data/qianxi_lay.mp4")
    os.system("ffmpeg -y -i ./data/qianxi_lay.mp4 -i ./data/han.mp4 -filter_complex 'overlay=410:1140' ./data/han_lay.mp4")
    # code = os.system(
    #     f"ffmpeg -y -threads {t_num} -i {dir_m1} -i {dir_m2} "
    #     f"-filter_complex 'overlay={left_m2}:{top_m2}' -loglevel error {mid_dir}")
if __name__ == '__main__':
    main()
    # data = [
    #     'videos': [{'top': 1140, 'url': 'han', 'crop': {'top': 0, 'left': -76, 'width': 518, 'height': 648}, 'left': 410, 'text': {}, 'width': 300, 'height': 375, 'duration': 5, 'layer_order': 7},
    #                {'top': 977, 'url': 'qanxi', 'crop': {'top': 0, 'left': -76, 'width': 518, 'height': 648}, 'left': 55, 'text': {}, 'width': 300, 'height': 375, 'duration': 5, 'layer_order': 3}],
    # {'top': 0, 'crop': {}, 'left': 0, 'text': {}, 'width': 1080, 'height': 1920, 'duration': 30, 'layer_order': 0}]