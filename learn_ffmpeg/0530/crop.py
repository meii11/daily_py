#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/05/30
"""
import os

def main():
    video = './data/video.mp4'
    bg = './data/bg.jpg'

    os.system("ffmpeg -y -i ./data/video.mp4 -vf crop=w=432:h=777:x=0:y=0 ./data/crop_front.mp4")
    # os.system("ffmpeg -y -i ./data/crop_front.mp4 -vf scale=1065=1915 ./data/resize_front.mp4")
    # os.system(
    #     f"ffmpeg -y -i ./data/crop_front.mp4 -vf 'scale=1066:1916,setsar=1' ./data/resize_front.mp4")

if __name__ == '__main__':
    main()
    da = {'fps': 30, 'stories':
        [{'fps': 30, 'order': 1,
          'lay_out': {'text': [], 'charts': [],
                      'images': [{'top': 0,
                                  'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/bg_import_1652339586034.jpg', 'crop': {}, 'left': 0, 'text': {}, 'width': 1080, 'height': 1920, 'duration': 30, 'layer_order': 0}],
                      'videos': [{'top': 0, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/video-ele1653896530940',
                                  'crop': {'top': -4, 'left': 0, 'width': 432, 'height': 777},
                                  'left': 0, 'text': {}, 'width': 1065, 'height': 1915, 'duration': 5, 'layer_order': 3}],
                      'persons': [{'id': 'huayuan8_mouth', 'top': 985, 'crop': {'top': 0, 'left': 0, 'width': 768, 'circle': 'false', 'height': 768}, 'left': 77, 'text': {'content': '但跟普通商保不一样，沪惠保不限年龄、不限健康状况、不限户籍、不限职业。'}, 'audio': 'aishuo', 'speed': 1.25, 'width': 927, 'height': 927, 'duration': 5, 'layer_order': 4}]}, 'batch_no': '980860854285107200'}], 'batch_no': '980860854285107200', 'resolution': '1080*1920', 'video_type': 'mp4', 'base': '/data/caopei/1-code/BackgroungCombination_chopei/local/980860854285107200'}