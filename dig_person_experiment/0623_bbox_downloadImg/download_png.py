#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/23
"""


def main():
    import requests
    from PIL import Image
    url = 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655796893482'
    im = Image.open(requests.get(url, stream=True).raw)
    im.save("123.png")


if __name__ == '__main__':
    main()
    d = {'fps': 25, 'stories': [{'fps': 25, 'order': 1, 'lay_out': {'text': [], 'charts': [], 'images': [
        {'top': 0, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/bg_import_1652364799571.jpg', 'crop': {}, 'left': 0, 'text': {}, 'width': 1920, 'height': 1080, 'duration': 30, 'layer_order': 0},
        {'top': 355, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655796893482', 'crop': {'top': 499, 'left': 550, 'width': 4400, 'height': 4000}, 'left': 175, 'text': {}, 'width': 490, 'height': 653, 'duration': 5, 'layer_order': 1}, {'top': 350, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655796907455', 'crop': {'top': 499, 'left': 550, 'width': 4400, 'height': 4000}, 'left': 718, 'text': {}, 'width': 465, 'height': 630, 'duration': 5, 'layer_order': 5}, {'top': 648, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655796916133', 'crop': {'top': 499, 'left': 550, 'width': 4400, 'height': 4000}, 'left': 1223, 'text': {}, 'width': 578, 'height': 365, 'duration': 5, 'layer_order': 7}], 'videos': [], 'persons': [{'id': '007red', 'top': 0, 'crop': {'top': 114, 'left': 111, 'width': 577, 'circle': 'false', 'height': 811}, 'left': 1770, 'text': {'content': '测试'}, 'audio': 'maoxiaomei', 'speed': 1, 'width': 150, 'height': 210, 'duration': 5, 'layer_order': 4}]}, 'batch_no': '988831590471696384'}], 'batch_no': '988831590471696384', 'resolution': '1920*1080', 'video_type': 'mp4', 'time_now': '22_45_10', 'base': '/data/caopei/1-code/0_BGC_chopei/local/988831590471696384'}