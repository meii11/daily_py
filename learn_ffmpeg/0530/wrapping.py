#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/05/30
"""
import os


def main():
    os.system(
        "ffmpeg -i ./data/video.mp4 -vf "
        "'[in]drawtext=fontsize=20:fontcolor=Black:fontfile='./data/simsun.ttc':text='onLine1':x=(w)/2:y=(h)/2,"
        "drawtext=fontsize=20:fontcolor=Black:fontfile='./data/simsun.ttc':text='onLine2':x=(w)/2:y=((h)/2)+25,"
        "drawtext=fontsize=20:fontcolor=Black:fontfile='./data/simsun.ttc':text='onLine3':x=(w)/2:y=((h)/2)+50[out]' "
        "-y test_out.avi")


if __name__ == '__main__':
    main()
    # a = "ffmpeg -i test_in.avi -vf "[in]drawtext=fontsize=20:fontcolor=White:fontfile='/Windows/Fonts/arial.ttf':text='onLine1':x=(w)/2:y=(h)/2, drawtext=fontsize=20:fontcolor=White:fontfile='/Windows/Fonts/arial.ttf':text='onLine2':x=(w)/2:y=((h)/2)+25, drawtext=fontsize=20:fontcolor=White:fontfile='/Windows/Fonts/arial.ttf':text='onLine3':x=(w)/2:y=((h)/2)+50[out]" -y test_out.avi"