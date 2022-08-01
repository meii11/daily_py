#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/07/21
"""
import glob
import os.path
import requests
import ffmpeg


def main():
    data_dir = glob.glob('../../dig_data/*txt')

    for data in data_dir:
        get_data(data)


def get_data(txt):
    link = open(txt, 'r').readlines()[1].rstrip()

    video_dir, video_name = os.path.split(txt)
    video_name = video_name.split('.')[0]

    _download_video(link, os.path.join(video_dir, video_name + '.mp4'))


def _download_video(url, output_dir):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 ",
    }
    video_code = -1
    ind = 0
    while not os.path.isfile(output_dir):
        # while video_code == 200:
        video = requests.get(url, headers=headers)
        video_code = video.status_code

        with open(output_dir, "wb") as video_file:
            video_file.write(video.content)


if __name__ == '__main__':
    main()
