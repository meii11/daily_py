#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/07/28
"""
import cv2
import numpy as np
def main():
    matte = cv2.imread('matte.png')
    origin = cv2.imread('original.png')

    mask = matte > 200.0

    b_channel, g_channel, r_channel = cv2.split(origin)
    alpha_channel = np.full(b_channel.shape, 255.0)
    alpha = np.array(mask[:, :, 0] * alpha_channel, dtype=b_channel.dtype)

    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha))
    cv2.imwrite('123.png', img_BGRA)
    print('1')


if __name__ == '__main__':
    main()
