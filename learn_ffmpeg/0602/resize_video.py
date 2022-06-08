#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/02
"""
import os


def main():
    img = './data/1654141350728.jpg'

    os.system(f"ffmpeg -i ./data/1654141350728.jpg -vf scale=1080:1920 ./data/123.png")


if __name__ == '__main__':
    main()
