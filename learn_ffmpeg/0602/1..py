#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/02
"""
import cv2


def main(crop, image, resize):
    image = cv2.imread("./2.png")

    if crop:
        top, left, width, height = crop['top'], crop['left'], crop['width'], crop['height']
        image = image[top:top + height, left:left + width]
    cv2.imwrite("123.png", image)
    image = cv2.resize(image, [resize[0], resize[1]])

    cv2.imwrite('./qianxi123.png', image)


if __name__ == '__main__':
    data = {'top': 1582, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1654135439386', 'crop': {'top': 12, 'left': 12, 'width': 230, 'height': 230}, 'left': 362, 'text': {}, 'width': 360, 'height': 332, 'duration': 5, 'layer_order': 26}

    main(data['crop'], '', [data['width'], data['height']])
