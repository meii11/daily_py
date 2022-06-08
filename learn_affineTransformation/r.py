#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/05/15
"""
import cv2


def main():
    img = cv2.imread("1.png")
    h, w = img.shape[:2]

    target = (112, 96)

    # w / h
    t_ratio = 112 / 96

    h_new = w / 112 * 96


    print("1")

if __name__ == '__main__':
    main()
