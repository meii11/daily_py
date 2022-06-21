#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/05/27
"""

import numpy as np
import cv2


def main():
    # img = np.zeros((2000, 2000, 3), dtype=np.uint8)
    # cv2.circle(img, (1000, 1000), 1000, (255, 255, 255), -1)
    #
    #
    # v = cv2.VideoCapture('female_desk.mp4')
    # ret, frame = v.read()
    # # frame = s
    #
    # cv2.imwrite("test.png", frame)

    frame = cv2.imread("test.png")

    frame = frame[340:, 14:754, ]
    cv2.imwrite("re.png", frame)

    b_channel, g_channel, r_channel = cv2.split(frame)
    alpha_channel = np.full(b_channel.shape, 255.0)

    cir = cv2.imread("img.png")
    cir = cv2.resize(cir, [740, 740])
    mask = cir >= 200.0

    alpha = np.array(mask[:, :, 0] * alpha_channel, dtype=b_channel.dtype)
    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha))

    cv2.imwrite("ccc.png", img_BGRA)


if __name__ == '__main__':
    main()
