#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/10
"""
import os

import cv2


def main():
    video = cv2.VideoCapture('../data/4_2_677_dig.mp4')
    ret, frame = video.read()
    height, width = frame.shape[:2]

    half_w = width // 2
    frame_normal, frame_mask = frame[:, :half_w, :], frame[:, half_w:, :]
    crop = {'top': 55, 'left': 39, 'width': 113, 'circle': 'true', 'height': 113}
    cv2.imwrite('../data/formal.png', frame_normal)
    os.system(f"ffmpeg -i ../data/formal.png -vf 'drawbox=x=238:y=100:w=222:h=222:color=red@0.5' ../data/drawbox.png")
    # crop_frame = frame_normal[crop['top']:crop['top'] + crop['height'],
    #              crop['left']:crop['left'] + crop['width']]
    # cv2.imwrite('../data/after_crop.png', crop_frame)


if __name__ == '__main__':
    main()
    # {'id': 'huayuan8_mouth', 'top': 2, 'crop': {'top': 55, 'left': 39, 'width': 113, 'circle': 'true', 'height': 113},
    #  'left': 677, 'text': {'content': '测试文本框的输入效果，所以文案不重要'}
