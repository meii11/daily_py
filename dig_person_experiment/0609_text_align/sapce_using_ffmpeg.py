#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/14
"""
import os

def main():
    code = os.system(
        f"ffmpeg -y -threads 6 -i ../data/white_bkg_1080_1920.jpg -vf "
        f"'drawtext=text='  你好':expansion=normal:fontfile=../data/font/simsun.ttc"
        # f":y={self.t_top}:x=({self.t_width}-text_w)/2+{self.t_left}:"
        f":y=50:x=50:"
        f"fontcolor=red:fontsize=55' -loglevel error ../data/white_bkg1234.jpg")


if __name__ == '__main__':
    main()
