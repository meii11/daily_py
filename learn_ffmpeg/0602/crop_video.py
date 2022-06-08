#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/02
"""
import os
import numpy as np
import cv2
import ffmpeg
t_num = 8
class VideoCrop:
    def run(self, video_dir, bound_size, base_dir, output_dir):
        base_dir_tmp = os.path.join(base_dir, 'crop_video')
        if not os.path.exists(base_dir_tmp):
            os.makedirs(base_dir_tmp)
        alpha_dir = self._create_alpha_img(bound_size, base_dir_tmp)
        resize_video_dir, pos = self._resize_video(video_dir, bound_size, base_dir_tmp)
        self._merge_video_alpha(alpha_dir, resize_video_dir, pos, output_dir)

    def _create_alpha_img(self, video_size, base_dir):
        width, height = video_size
        img = np.zeros((width, height, 4))
        cv2.imwrite(os.path.join(base_dir, "alpha.png"), img)
        return os.path.join(base_dir, "alpha.png")

    def _resize_video(self, video_dir, bound_size, base_dir):
        c_height, c_width = bound_size
        v_info = ffmpeg.probe(video_dir)['streams'][0]


        v_width, v_height = v_info['width'], v_info['height']

        # 等比扩大or缩小
        if v_width > v_height:  # 如果长边是宽
            ratio = v_width / v_height

            v_width = c_width if c_width % 2 == 0 else c_width + 1
            v_height = int(v_width / ratio) if int(v_width / ratio) % 2 == 0 else int(v_width / ratio) + 1
            pos = [(c_height - v_height) // 2, 'width']
        else:
            ratio = v_width / v_height
            v_height = c_height if c_height % 2 == 0 else c_height + 1
            v_width = int(ratio * v_height) if int(ratio * v_height) % 2 == 0 else int(ratio * v_height) + 1
            pos = [(c_width - v_width) // 2, "height"]
        mid_video_dir = video_dir.split("/")[-1].split(".mp4")[0] + "_resize.mp4"

        os.system(f"ffmpeg -y -threads {t_num} -i {video_dir} -vf 'scale={v_width}:{v_height}' -loglevel error {os.path.join(base_dir, mid_video_dir)}")

        return os.path.join(base_dir, mid_video_dir), pos

    def _merge_video_alpha(self, alpha_dir, video_dir, pos, output_dir):
        if pos[1] == 'height':  # 表示高是一样的
            left = pos[0]
            top = 0
        else:  # 宽一样
            left = 0
            top = pos[0]
        # -filter_complex 'overlay={left_m2}:{top_m2}' -loglevel error {mid_dir}
        # mid_video_dir = video_dir.split("/")[-1].split(".mp4")[0] + "_crop.mov"
        # output_dir = os.path.join(base_dir, mid_video_dir)
        os.system(
            f"ffmpeg -y -threads {t_num} -i {alpha_dir} -i {video_dir} -filter_complex 'overlay={left}:{top}' -vcodec qtrle -loglevel error {output_dir}")


if __name__ == '__main__':
    a = [
        {'top': 500,
         'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/video-ele1654150705299',
         'crop': {'top': 0, 'left': -76, 'width': 518, 'height': 648}, 'left': 250, 'text': {}, 'width': 300, 'height': 375, 'duration': 5, 'layer_order': 3}]
    VideoCrop().run('./qianxi.mp4', [300, 375], './data', './123.mov')