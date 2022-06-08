#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/01
"""
import os
import requests
import time


def main():
    # code = -1
    # ind = 0
    # while code != 0:
    #     code = os.system(
    #         f"ffmpeg -y -i spirite_away.mp -map 0:v -vcodec copy ./1.mp4 -map 0:a -acodec copy -loglevel error 2.aac")
    #     print(ind)
    #     ind += 1

    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 ",
    # }
    # video_code = -1
    # ind = 0
    # while video_code == 200:
    #     video = requests.get("https://public-1255423687.cos.ap-shanghai.myqcloud.com/video-ele1654051280825", headers=headers)
    #     video_code = video.status_code
    #     ind += 1
    # with open("123.mp4", "wb") as video_file:
    #     video_file.write(video.content)
    time1 = time.localtime(time.time())
    print(time1.tm_hour)


if __name__ == '__main__':
    main()
    data = [
        {'top': 1140, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/video-ele1654069621083', 'crop': {'top': 0, 'left': -76, 'width': 518, 'height': 648}, 'left': 410, 'text': {}, 'width': 300, 'height': 375, 'duration': 5, 'layer_order': 7},
        {'top': 977, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/video-ele1654069616963', 'crop': {'top': 0, 'left': -76, 'width': 518, 'height': 648}, 'left': 55, 'text': {}, 'width': 300, 'height': 375, 'duration': 5, 'layer_order': 3},
    {'top': 0, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/bg_import_1652339586034.jpg', 'crop': {}, 'left': 0, 'text': {}, 'width': 1080, 'height': 1920, 'duration': 30, 'layer_order': 0}]