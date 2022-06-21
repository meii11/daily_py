#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/21
"""
import cv2
import numpy as np


def main():
    r = np.full((500, 500, 1), 255.0)
    g = np.full((500, 500, 1), 255.0)
    b = np.full((500, 500, 1), 255.0)

    alpha = np.full((500, 500, 1), 100.0)
    img = cv2.merge((b, g, r, alpha))
    cv2.imwrite("white.png", img)
    pass


if __name__ == '__main__':
    main()
