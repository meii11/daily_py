#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/21
"""
import os


def main():
    os.system(f"ffmpeg -y -i 123.jpg -i 1.png "
              f"-filter_complex '[0]scale=600:600[b];[b][1]overlay=0:0[v]' -map [v] 123123.png")


if __name__ == '__main__':
    main()
