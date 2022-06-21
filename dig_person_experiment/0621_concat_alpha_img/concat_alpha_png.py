#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/21
"""


def main():
    os.system("ffmpeg -y -i ./qiyu_500.png -vf crop=3000:3000:0:0 ./circle_data/bkg_square.png")


if __name__ == '__main__':
    main()
