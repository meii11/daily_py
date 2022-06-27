#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/26
"""

import os
import numpy as np
import cv2


def random_dilate(alpha, low=1, high=5, mode='constant'):
    """Dilation. erode"""
    iterations = np.random.randint(1, 20)
    erode_ksize = np.random.randint(low=low, high=high)
    dilate_ksize = np.random.randint(low=low, high=high)
    erode_kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (erode_ksize, erode_ksize))  # 椭圆 (尺寸)
    dilate_kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (dilate_ksize, dilate_ksize))
    alpha_eroded = cv2.erode(alpha, erode_kernel, iterations=iterations)
    alpha_dilated = cv2.dilate(alpha, dilate_kernel, iterations=iterations)
    if mode == 'constant':
        alpha_noise = 128 * np.ones_like(alpha)
        alpha_noise[alpha_eroded >= 255] = 255  ###250
        alpha_noise[alpha_dilated <= 0] = 0
    else:
        value = np.random.randint(low=100, high=255)
        alpha_noise = value * ((alpha_dilated - alpha_eroded) / 255.)
        alpha_noise += alpha_eroded
    return alpha_noise
