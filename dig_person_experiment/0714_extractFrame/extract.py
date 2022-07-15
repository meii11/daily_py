#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/07/14
"""
import os
import ffmpeg
from tqdm import tqdm


def main():
    file_dir = '../../../digPerson_dataset'

    for _, _, files in os.walk(file_dir):
        for file in tqdm(files):
            if 'mp4' not in file:
                continue
            extract_frame(file, file_dir)


def extract_frame(video_dir, base_dir):
    save_dir = os.path.join(base_dir, os.path.splitext(video_dir)[0])
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    video_dir = os.path.join(base_dir, video_dir)
    info = ffmpeg.probe(video_dir)
    video_stream = next((stream for stream in info['streams'] if stream['codec_type'] == 'video'), None)
    fps = int(eval(video_stream['r_frame_rate']))  # 实时帧率

    code = os.system(
        f"ffmpeg -threads 16 -y -i {video_dir} -start_number 0 -r '{fps}/1' -loglevel error '{save_dir}/%06d.png'")


if __name__ == '__main__':
    main()
