#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/07/12
"""
import cv2

def main():
    video = cv2.VideoCapture('123.mp4')
    ret, frame = video.read()
    cv2.imwrite('123.png', frame)


if __name__ == '__main__':
    main()
