#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/21
"""
import os


def main():
    # os.system("ffmpeg -y -i ./qiyu_500.png -vf crop=3000:3000:0:0 ./circle_data/bkg_square.png")
    os.system(f"ffmpeg -i dwOWes8ZPMU.jpg -i qiyu_500.png -filter_complex overlay=500:500 final.png")


if __name__ == '__main__':
    main()
