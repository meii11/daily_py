#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/20
"""
import os

def main(info, ind):
    if ind == 1:
        os.system(f"ffmpeg -y -i bg_import_1652364804024.jpg -vf 'drawbox=x={info['left']}:y={info['top']}:w={info['width']}:h={info['height']}:color=red' -loglevel error "
                  f"final_{ind}.png")
    else:
        os.system(
            f"ffmpeg -y -i final_{ind - 1}.png -vf 'drawbox=x={info['left']}:y={info['top']}:w={info['width']}:h={info['height']}:color=red' -loglevel error "
            f"final_{ind}.png")
if __name__ == '__main__':
    d = [

                 {'top': 820, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655692756801', 'crop': {'top': 553, 'left': -335, 'width': 1782, 'height': 1228}, 'left': 1128, 'text': {}, 'width': 248, 'height': 100, 'duration': 5, 'layer_order': 8},
                 {'top': 210, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655692666356', 'crop': {'top': -516, 'left': 11, 'width': 708, 'height': 3636}, 'left': 1390, 'text': {}, 'width': 165, 'height': 300, 'duration': 5, 'layer_order': 7},
                 {'top': 525, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655692847260', 'crop': {'top': 1638, 'left': -853, 'width': 5120, 'height': 3481}, 'left': 553, 'text': {}, 'width': 298, 'height': 300, 'duration': 5, 'layer_order': 9},
                 {'top': 695, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655692693026', 'crop': {'top': -726, 'left': 534, 'width': 3968, 'height': 2806}, 'left': 1133, 'text': {}, 'width': 250, 'height': 100, 'duration': 5, 'layer_order': 6},
                 {'top': 210, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655692687558', 'crop': {'top': -617, 'left': 432, 'width': 1822, 'height': 3702}, 'left': 1595, 'text': {}, 'width': 138, 'height': 300, 'duration': 5, 'layer_order': 10},
                 {'top': 955, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655692766487', 'crop': {'top': 1037, 'left': 0, 'width': 3600, 'height': 1122}, 'left': 1133, 'text': {}, 'width': 250, 'height': 100, 'duration': 5, 'layer_order': 11},
                 {'top': 185, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655692680393', 'crop': {'top': 173, 'left': 0, 'width': 4000, 'height': 1686}, 'left': 863, 'text': {}, 'width': 303, 'height': 300, 'duration': 5, 'layer_order': 5},
                 {'top': 355, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655692638384', 'crop': {'top': 217, 'left': 619, 'width': 2096, 'height': 2939}, 'left': 735, 'text': {}, 'width': 250, 'height': 300, 'duration': 5, 'layer_order': 1}]

    ind = 1
    for dd in d:
        main(dd, ind)
        ind += 1