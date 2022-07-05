#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/07/05
"""
import ffmpeg
import cv2
import numpy as np

def main():
    # info = ffmpeg.probe('./175253.jpg')
    # info1 = ffmpeg.probe('./kaori.jpeg')
    # info2 = ffmpeg.probe('./迪卢克凯亚-750x1334.png')
    # pass
    vid_cap = cv2.VideoCapture('./spirite_away.mp4')
    ret, tmp_frame = vid_cap.read()
    pixel = tmp_frame[0][0]
    v_frame_width = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    v_frame_height = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    img = np.zeros((v_frame_height, v_frame_width, 3), np.uint8)
    img_rgb = img.copy()
    img_rgb[:, :, :] = pixel
    cv2.imwrite("green_new.png", img_rgb)
    vd_bgr_img = './green.png'

if __name__ == '__main__':
    main()
