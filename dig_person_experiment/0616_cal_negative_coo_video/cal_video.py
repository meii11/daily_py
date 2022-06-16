#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/16
"""
import ffmpeg
import os


def _cal_new_coo(video_dir, crop_coo, full_coo, output_dir):
    v_info = ffmpeg.probe(video_dir)['streams'][0]
    v_width, v_height = v_info['width'], v_info['height']

    crop_width, crop_height = crop_coo['width'], crop_coo['height']

    w_h_ratio = v_width / v_height

    # 如果高是长边
    if v_height > v_width:
        # 因为视频resize需要偶数边，因此需要做一个判断
        v_height = crop_height if crop_height % 2 == 0 else crop_height + 1
        v_width = int(w_h_ratio * v_height) if int(w_h_ratio * v_height) % 2 == 0 else int(w_h_ratio * v_height) + 1

        new_top = full_coo['top']
        new_left = (crop_width - v_width) // 2 + full_coo['left']
    # 宽是长边同理，这里包含了高宽相同的情况
    else:
        v_width = crop_width if crop_width % 2 == 0 else crop_width + 1
        v_height = int(v_width / w_h_ratio) if int(v_width / w_h_ratio) % 2 == 0 else int(v_width / w_h_ratio) + 1

        new_top = (crop_height - v_height) // 2 + full_coo['top']
        new_left = full_coo['left']

    # step1 resize video and output to final output
    base_dir, file_name = os.path.split(output_dir)
    layer_order = file_name.split("_")[0]
    output_dir = os.path.join(base_dir, f"{layer_order}_{new_top}_{new_left}_video.mp4")
    os.system(f"ffmpeg -i {video_dir} -vf scale={v_width}:{v_height} -loglevel error {output_dir}")


def main():
    pass


if __name__ == '__main__':
    main()
