#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/06
"""

import os

import ffmpeg
import numpy as np
import cv2
import psutil

t_num = psutil.cpu_count(False)
# t_num = 20


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
        img = np.zeros((height, width, 4))
        cv2.imwrite(os.path.join(base_dir, "alpha.png"), img)
        return os.path.join(base_dir, "alpha.png")

    def _resize_video(self, video_dir, bound_size, base_dir):
        c_width, c_height = bound_size
        v_info = ffmpeg.probe(video_dir)['streams'][0]

        v_width, v_height = v_info['width'], v_info['height']

        # 等比扩大or缩小
        if v_width > v_height:  # 如果长边是宽
            ratio = v_width / v_height

            v_width = c_width if c_width % 2 == 0 else c_width + 1
            v_height = int(v_width / ratio) if int(v_width / ratio) % 2 == 0 else int(v_width / ratio) + 1
            pos = [(c_height - v_height) // 2, 'width'] if (c_height - v_height) > 0 else [0, 'width']
        else:
            ratio = v_width / v_height
            v_height = c_height if c_height % 2 == 0 else c_height + 1
            v_width = int(ratio * v_height) if int(ratio * v_height) % 2 == 0 else int(ratio * v_height) + 1
            pos = [(c_width - v_width) // 2, "height"] if (c_width - v_width) > 0 else [0, 'height']
        mid_video_dir = video_dir.split("/")[-1].split(".mp4")[0] + "_resize.mp4"

        os.system(
            f"ffmpeg -y -threads {t_num} -i {video_dir} -vf 'scale={v_width}:{v_height}' -loglevel error {os.path.join(base_dir, mid_video_dir)}")

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
        # if top == left == 0:
        #     os.system()
        os.system(
            f"ffmpeg -y -threads {t_num} -i {alpha_dir} -i {video_dir} -filter_complex 'overlay=-1:0' -vcodec qtrle -loglevel error {output_dir}")


def dig_resize():
    img = './hhh.mp4'

    os.system('ffmpeg -i ./video.mp4 -vf crop=w=577:h=811:x=111:y=114 ./hhh1.mp4')
    os.system('ffmpeg -i ./hhh1.mp4 -vf scale=528:528 ./hhh2.mp4')

    # crop=w={width}:h={height}:x={left}:y={top}


if __name__ == '__main__':
    d = {'fps': 25, 'stories': [
        {'fps': 25, 'order': 1,
         'lay_out': {'text': [], 'charts': [],
                     'images': [
                         {'top': 0,
                          'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/bg_import_1652339584987.jpg',
                          'crop': {}, 'left': 0, 'text': {}, 'width': 1920, 'height': 1080, 'duration': 30,
                          'layer_order': 0}],
                     'videos': [
                         {'top': 0,
                          'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/video-ele1654485435152',
                          'crop': {'top': 0, 'left': 0, 'width': 614, 'height': 345}, 'left': 0, 'text': {},
                          'width': 1915, 'height': 1075, 'duration': 5, 'layer_order': 3}],
                     'persons': [{'id': '007red', 'top': 545,
                                  'crop': {'top': 114, 'left': 111, 'width': 577, 'circle': 'false', 'height': 811},
                                  'left': 1382, 'text': {
                             'content': '哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈'},
                                  'audio': 'rosa', 'speed': 1, 'width': 527, 'height': 527, 'duration': 5,
                                  'layer_order': 4}]}, 'batch_no': '983330686247108608'}],
         'batch_no': '983330686247108608', 'resolution': '1920*1080', 'video_type': 'mp4', 'time_now': '11_19_11',
         'base': '/data/caopei/1-code/BackgroungCombination_chopei/local/983330686247108608'}

    # VideoCrop().run(video_dir='./1.mp4', bound_size=[1915, 1075], base_dir='', output_dir='./111.mov')
    # os.system('ffmpeg -i ./1.mp4 -vf scale=1916:1076 ./2.mp4')
    dig_resize()
    # dd = 'persons': [{'id': '007red', 'top': 545,
    #                               'crop': {'top': 114, 'left': 111, 'width': 577, 'circle': 'false', 'height': 811},
    #                               'left': 1382, 'text': {
    #                          'content': '哈哈哈哈哈哈哈'},
    #                               'audio': 'rosa', 'speed': 1, 'width': 527, 'height': 527, 'duration': 5,
    #                               'layer_order': 4}]}, 'batch_no': '983330686247108608'}

    # d = {'fps': 25, 'stories': [{'fps': 25, 'order': 1, 'lay_out': {'text': [], 'charts': [], 'images': [{'top': 0, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/bg_import_1652339584987.jpg', 'crop': {}, 'left': 0, 'text': {}, 'width': 1920, 'height': 1080, 'duration': 30, 'layer_order': 0}], 'videos': [{'top': 0, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/video-ele1654500931100', 'crop': {'top': 0, 'left': -1, 'width': 1382, 'height': 776}, 'left': 0, 'text': {}, 'width': 1915, 'height': 1075, 'duration': 5, 'layer_order': 3}],
    #                                                                 'persons': [{'id': '007red', 'top': 545, 'crop': {'top': 114, 'left': 111, 'width': 577, 'circle': 'false', 'height': 811}, 'left': 1382, 'text': {'content': '中国青年报客户端北京6月6日电（中青报·中青网记者 邱晨辉）据中国载人航天工程办公室消息，已进驻中国空间站天和核心舱的神舟十四号航天员乘组，于北京时间2022年6月6日11时9分成功开启天舟四号货物舱舱门，在完成环境检测等准备工作后，于12时19分顺利进入天舟四号货运飞船。\n\n6月5日10时44分，搭载神舟十四号载人飞船的长征二号F遥十四运载火箭点火发射，约577秒后，神舟十四号载人飞船与火箭成功分离，进入预定轨道。飞行乘组状态良好，发射取得圆满成功。\n\n这是我国载人航天工程立项实施以来的第23次飞行任务，也是空间站阶段的第3次载人飞行任务。\n\n当天，在神舟十四号载人飞船与空间站组合体成功实现自主快速交会对接后，航天员乘组从返回舱进入轨道舱。按程序完成各项准备后，航天员陈冬成功开启天和核心舱舱门，北京时间2022年6月5日20时50分，航天员陈冬、刘洋、蔡旭哲依次进入中国空间站天和核心舱，正式开启为期6个月的在轨驻留。\n\n接下来，航天员乘组还将进入天舟三号货运飞船。后续，航天员乘组将按计划开展货物转运等相关工作。'},
    #                                                                              'audio': 'rosa', 'speed': 1, 'width': 527, 'height': 527, 'duration': 5, 'layer_order': 4}]}, 'batch_no': '983395706393853952'}], 'batch_no': '983395706393853952', 'resolution': '1920*1080', 'video_type': 'mp4', 'time_now': '15_38_4', 'base': '/data/caopei/1-code/BackgroungCombination_chopei/local/983395706393853952'}