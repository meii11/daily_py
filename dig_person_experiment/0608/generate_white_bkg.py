#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/08
"""
import numpy as np
import cv2

def _gen_white_bkg(resolution):
    bkg = np.full((resolution[1], resolution[0]), 255)

    # 高、宽
    cv2.imwrite('white_bkg.png', bkg)

    pass

if __name__ == '__main__':
    _gen_white_bkg(resolution=[1920, 1080])
