#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/06
"""
import numpy as np
import cv2
def main():
    width, height = 875, 500
    img = np.zeros((width, height, 4))
    cv2.imwrite("alpha.png", img)

if __name__ == '__main__':
    main()
