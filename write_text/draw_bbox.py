#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/07/15
"""
import os


def main():
    video = './data_for_test/997456569845153792_15.mp4'

    out = './result/bbox.mp4'

    crop = {"top": 370, "left": 100, "width": 900, "height": 1490}
    # img = '1655962817493.jpg'
    # [370, 100, 900, 1490]
    os.system(
        f"ffmpeg -y -i {video} -vf 'drawbox=x={crop['left']}:y={crop['top']}:w={crop['width']}:h={crop['height']}:color=red' -loglevel error "
        f"{out}")


if __name__ == '__main__':
    main()
