#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/09
"""
import ffmpeg
from PIL import Image, ImageDraw, ImageFont
import os
import cv2
import psutil
import numpy as np

# t_num = psutil.cpu_count(False)
t_num = 20


class TextTools:

    def __init__(self, font, font_size, width):
        self.font = ImageFont.truetype(font, font_size)
        self.width = width
        # 预设宽度 可以修改成你需要的图片宽度
        # self.width = 300
        # # 文本
        # self.text = text
        # # 段落 , 行数, 行高
        # self.duanluo, self.note_height, self.line_height = self.split_text()

    def get_paragraph(self, text):
        # 这里预设一个用于写字的工具变量
        txt = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)

        paragraph = ""
        sum_width = 0
        line_count = 1
        line_height = 0

        for char in text:
            width, height = draw.textsize(char, self.font)
            sum_width += width
            if sum_width > self.width:  # 超过预设宽度就修改段落 以及当前行数
                line_count += 1
                sum_width = 0
                paragraph += '\n'
            paragraph += char
            line_height = max(height, line_height)
        if not paragraph.endswith('\n'):
            paragraph += '\n'
        return paragraph, line_height, line_count

    def split_text(self, content):
        # 按规定宽度分组
        max_line_height, total_lines = 0, 0
        allText = []
        for text in content.split('\n'):
            duanluo, line_height, line_count = self.get_paragraph(text)
            max_line_height = max(line_height, max_line_height)
            total_lines += line_count
            allText.append((duanluo, line_count))
        line_height = max_line_height
        total_height = total_lines * line_height
        return allText, total_height, line_height, total_lines

    def draw_text(self, allText, line_height, input_dir, font_color, pos):

        # note_img = Image.open(input_dir).convert("RGBA")
        note_img = input_dir
        draw = ImageDraw.Draw(note_img)
        # 左上角开始
        x, y = pos
        for duanluo, line_count in allText:
            draw.text((x, y), duanluo, fill=font_color, font=self.font)
            y += line_height * line_count

        return note_img


class TextWriter:
    def __init__(self, content, loc, font_type, fontsize, font_color, input_dir, output_dir):
        self.content = content
        self.t_top, self.t_left, self.t_width, self.t_height = loc
        self.font_type = font_type
        self.font_size = fontsize
        self.font_color = font_color
        self.intput_dir = input_dir
        self.output_dir = output_dir

        self.media_type = 'png' if 'png' in self.output_dir else "mp4"

    def _hex_to_rgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def run(self):
        self._perprocess()

    def _perprocess(self):
        text_tools = TextTools(font=self.font_type, font_size=self.font_size, width=self.t_width)
        allText, total_height, line_height, total_lines = text_tools.split_text(self.content)
        if total_lines == 1:  # 如果是一行
            con = self.content.replace(",", "\\\\\\,").replace("]", "\\\\\\]").replace("[", "\\\\\\["). \
                replace(";", "\\\\\\;").replace(":", "\\\\\\:").replace("<", "\\\\\\<").replace(">", "\\\\\\>") \
                .replace("?", "\\\\\\?").replace(".", "\\\\\\.").replace("\n", "")
            code = os.system(
                f"ffmpeg -y -threads {t_num} -i {self.intput_dir} -vf 'drawtext=text={self.content}:expansion=normal:fontfile={self.font_type}:y={self.t_top}:x=({self.t_width}-text_w)/2+{self.t_left}:fontcolor={self.font_color}:fontsize={self.font_size}' -loglevel error {self.output_dir}")
        else:
            if self.media_type == 'png':  # 图片直接写即可
                note_img = Image.open(self.intput_dir).convert("RGB")
                img = text_tools.draw_text(allText=allText, line_height=line_height, input_dir=note_img,
                                           font_color=self._hex_to_rgb(self.font_color), pos=[self.t_left, self.t_top])
                img.save(self.output_dir)
            else:
                video_info = ffmpeg.probe(self.intput_dir)['streams'][0]
                out_size = (video_info['width'], video_info['height'])
                v_writer = cv2.VideoWriter(self.output_dir, cv2.VideoWriter_fourcc(*'mp4v'), 25.0, tuple(out_size))
                video = cv2.VideoCapture(self.intput_dir)
                ret, frame = video.read()
                font_color = self.font_color.split("#")[1]
                # color = color.split("#")[1]
                c = []
                font_color = [font_color[i:i + 2] for i in range(0, len(font_color), 2)]
                font_color[0], font_color[2] = font_color[2], font_color[0]

                font_color = ''.join(font_color)
                while ret:
                    img = text_tools.draw_text(allText=allText, line_height=line_height,
                                               input_dir=Image.fromarray(frame),
                                               font_color=self._hex_to_rgb(font_color),
                                               pos=[self.t_left, self.t_top])

                    v_writer.write(np.array(img))
                    ret, frame = video.read()
                video.release()
                v_writer.release()


def main():
    font_color = '#000000'
    font_size = 14 * 3
    content = '发多少防守打法水电'
    t_top, t_left, t_width, t_height = 50+5, 500+5, 250, 100
    # font_type = '../data/font/SourceHanSans-Normal.ttc'
    font_type = '../data/font/simhei.ttf'

    # text_loc =
    # output_dir = '../data/test_0609_SourceHanSans.png'
    output_dir = '../data/test_0609_simhei.png'
    TextWriter(content=content, loc=[t_top, t_left, t_width, t_height], font_type=font_type, fontsize=font_size,
               font_color=font_color, input_dir='../data/white_bkg.jpg', output_dir=output_dir).run()

    # output_dir_box = '../data/test_0609_SourceHanSans_box.png'
    output_dir_box = '../data/test_0609_simhei_box.png'
    # os.system(f"ffmpeg -i {output_dir} -vf 'drawbox=500:50:250:100:red' {output_dir_box}")
    os.system(f"ffmpeg -y -i {output_dir} -vf 'drawbox=x=500:y=50:w=250:h=100:color=red@0.5' {output_dir_box}")
if __name__ == '__main__':
    # n = ImgText(
    #     "小编为大家讲解一下几位抗日名将的故事，第一位抗日名将杨靖宇，他不仅是白山黑水间的铁血将军，也是信念坚定的共产党员。他的威名，让敌人闻风丧胆，更令中国人骄傲。在1940"
    #     "年初，杨靖宇所带领的部队被日军围剿，他们已经断粮五天了，他和剩下的十几名战忍妥着饥饿，疲劳，与敌人奋战，后来其他战十都牺牲了，杨靖宇仍然边战边走。下面讲一讲狼牙山五壮士，1941年9月25"
    #     "日，数千名日伪军在河北易具狼牙山地区实施“清剿”。晋察冀一分区一团七连二排六班的5"
    #     "名战士，即班长马宝玉，副班长葛振林，战十胡德林、胡福才和宋学义，为掩护主力部队和群众转移，与敌人激烈战斗，利用有利地形奋勇还击，打日伪军多次进攻，毙伤90余人。第三个故事是刘胡兰的英雄事迹，1946年12"
    #     "月的一天，刘胡兰配合武工队员将“当地一害”石佩怀处死，阎锡山匪军恼羞成怒，决定实施报复行动。1947年1月12日，阎军突然袭击云周西村，刘胡兰因叛徒告密而被捕。刘胡兰烈士牺牲时，尚未满15"
    #     "周岁，是已知的中国共产党女烈十中年龄最小的一个。毛泽东在指挥全国战局之余，为刘胡兰题词:“生的伟大，死的光荣!")
    # n.draw_text()


    # aa ={'fps': 30, 'stories': [{'fps': 30, 'order': 1, 'lay_out': {'text': [
    #     {'top': 50, 'font': '黑体', 'left': 500, 'color': '#000000', 'width': 250, 'height': 100, 'content': '发多少防守打法水电', 'duration': 5, 'font_size': 13, 'layer_order': 2, 'is_animation': 'false'}
    # ], 'charts': [], 'images': [{'top': 0, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/bg_import_1652339584987.jpg', 'crop': {}, 'left': 0, 'text': {}, 'width': 1920, 'height': 1080, 'duration': 30, 'layer_order': 0}], 'videos': [], 'persons': [{'id': '007red', 'top': 500, 'crop': {'top': 25, 'left': 182, 'width': 476, 'circle': 'true', 'height': 476}, 'left': 625, 'text': {'content': '测试对齐'}, 'audio': 'laomei', 'speed': 1, 'width': 150, 'height': 150, 'duration': 5, 'layer_order': 4}]}, 'batch_no': '984434227887996928'}], 'batch_no': '984434227887996928', 'resolution': '1920*1080', 'video_type': 'mp4', 'time_now': '12_22_20', 'base': '/data/caopei/1-code/BackgroungCombination_chopei/local/984434227887996928'}

    main()
