#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/13
"""
import os


def main():
    video = '../data/short_video.mp4'
    mov_video = '../data/short_video_alpha.mov'
    mov2_video = '../data/short_video_alpha2.mov'
    audio = '../data/long_audio.aac'
    f_video = '../data/short_video_align.mov'
    # os.system(
        # f'ffmpeg -i {mov_video} -an -r 25 -filter:v "setpts=0.5*PTS" -vcodec qtrle {mov2_video}')

    code = os.system(f"ffmpeg -threads 6 -stream_loop -1 -i {mov2_video} -i {audio} "
                     f"-shortest -map 0:v:0 -map 1:a:0 -y -codec copy -q:v 1 "
                     f"-loglevel error -vcodec qtrle {f_video}")


if __name__ == '__main__':
    main()
