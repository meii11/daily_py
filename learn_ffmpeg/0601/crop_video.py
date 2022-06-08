#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/01
"""
import os

import numpy as np
import cv2


class VideoCrop:
    def run(self, video_dir, crop_size, video_size, base_dir):
        alpha_dir = self._create_alpha_img(crop_size, base_dir)
        resize_video_dir, pos = self._resize_video(video_dir, crop_size, video_size, base_dir)
        self._merge_video_alpha(alpha_dir, resize_video_dir, pos)

    def _create_alpha_img(self, crop_size, base_dir):
        left, top, width, height = crop_size
        img = np.zeros((width, height, 4))
        cv2.imwrite("./data/alpha.png", img)
        return "./data/alpha.png"

    def _resize_video(self, video_dir, crop_size, video_size, base_dir):
        _, _, c_width, c_height = crop_size
        v_width, v_height = video_size

        # 等比扩大or缩小
        if v_width > v_height:  # 如果长边是宽
            ratio = v_width / v_height

            v_width = c_width
            v_height = int(v_width / ratio) if int(v_width / ratio) % 2 == 0 else int(v_width / ratio) + 1
            pos = [(c_height - v_height) // 2, 'height']
        else:
            ratio = v_width / v_height
            v_height = c_height
            v_width = int(ratio * v_height) if int(ratio * v_height) % 2 == 0 else int(ratio * v_height) + 1
            pos = [(c_width - v_width) // 2, "width"]
        mid_video_dir = video_dir.split("/")[-1].split(".mp4")[0] + "_resize.mp4"
        os.system(f"ffmpeg -y -i {video_dir} -vf 'scale={v_width}:{v_height}' {os.path.join(base_dir, mid_video_dir)}")

        return os.path.join(base_dir, mid_video_dir), pos

    def _merge_video_alpha(self, alpha_dir, video_dir, pos):
        if pos[1] == 'height':
            height = pos[0]
            width = 0
        else:
            height = 0
            width = pos[0]
        # -filter_complex 'overlay={left_m2}:{top_m2}' -loglevel error {mid_dir}
        os.system(
            f"ffmpeg -y -i {alpha_dir} -i {video_dir} -filter_complex 'overlay={width}:{height}' -vcodec qtrle -loglevel error ./data/final.mov")


if __name__ == '__main__':

    data = [{'top': 500, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/video-ele1654150705299',
                       'crop': {'top': 0, 'left': -76, 'width': 518, 'height': 648}, 'left': 250, 'text': {}, 'width': 300, 'height': 375, 'duration': 5, 'layer_order': 3}
    VideoCrop().run(video_dir="./data/qianxi.mp4", crop_size=[0, 0, 518, 648], video_size=[720, 1280],
                    base_dir='./data')
