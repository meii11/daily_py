#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/14
"""
import os


def main():
    # os.system('ffmpeg -i hutao.png -vf scale=100:100 hutao_r.png')
    os.system('ffmpeg -i hutao.png hutao_r.jpeg')


if __name__ == '__main__':
    main()
