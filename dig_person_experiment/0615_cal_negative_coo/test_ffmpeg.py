#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/15
"""
import subprocess as sp
import numpy as np
import cv2
def main():

    command = ['ffmpeg',
               '-i', '../data/more2.mp4',
               '-f', 'image2pipe',
               '-pix_fmt', 'rgb24',
               '-vcodec', 'rawvideo', '-']
    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10 ** 8)

    # read 420*360*3 bytes (= 1 frame)
    raw_image = pipe.stdout.read(1080 * 1920 * 3)
    # transform the byte read into a numpy array
    image = np.fromstring(raw_image, dtype='uint8')
    image = image.reshape((1080, 1920, 3))
    # throw away the data in the pipe's buffer.
    # pipe.stdout.flush()
    cv2.imwrite("image.png", image)
    key = cv2.waitKey(0)
    pass

if __name__ == '__main__':
    main()
