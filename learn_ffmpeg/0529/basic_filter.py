#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/05/29
"""
import os


def main():
    os.system("ffmpeg -i ./data/spirite_away.mp4 -i ./data/kaori.jpeg -filter_complex '[1:v]scale=174:144[logo];[0:v][logo]overlay=x=0:y=0' output.mp4")


if __name__ == '__main__':
    main()
