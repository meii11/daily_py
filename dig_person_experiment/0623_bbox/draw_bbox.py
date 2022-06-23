#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/23
"""
import os

def main():
    crop = {"top": 34, "left": 0, "width": 370, "height": 208}
    img = '1655962817493.jpg'

    os.system(
        f"ffmpeg -y -i {img} -vf 'drawbox=x={crop['left']}:y={crop['top']}:w={crop['width']}:h={crop['height']}:color=red' -loglevel error "
        f"123.png")

if __name__ == '__main__':
    main()
