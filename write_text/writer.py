#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/07/05
"""
import json

import ffmpeg
from PIL import Image, ImageDraw, ImageFont
import os
import cv2
import psutil
import numpy as np

t_num = psutil.cpu_count(False)


# t_num = 20


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
        line_width = []  # 用于记录当前文本段中，每一行的宽度，两种情况会记录，一是长度到了自动换行时，二是到最后一个字了

        for ind in range(len(text)):
            if sum_width == 0 and text[ind] == ' ':
                continue
            tt = text[ind]
            width, height = draw.textsize(text[ind], self.font)

            sum_width += width
            paragraph += text[ind]
            line_height = max(height, line_height)
            if ind < len(text) - 1:
                next_width, _ = draw.textsize(text[ind + 1], self.font)
                if next_width == 0 and _ != 0:
                    next_width, _ = draw.textsize(text[ind], self.font)
            else:
                next_width = 0  # 最后一个字了
            if sum_width + next_width > self.width:  # 超过预设宽度就修改段落 以及当前行数
                # 但是当下一个字符为标点符号时，改字直接换行和下一个标点符号一起

                if ind < len(text) - 1 and text[ind + 1] in [',', '.', '，', '。', ':', '：']:
                    paragraph = ''.join(list(paragraph)[:-1])  # 该字段不计入
                    # text = list(text)
                    insert_text = list(text).copy()  # 将去掉的字加到下一行中
                    insert_text.insert(ind + 1, text[ind])
                    text = ''.join(insert_text)
                    sum_width -= width

                line_count += 1
                line_width.append(sum_width)
                sum_width = 0
                paragraph += '[split]'

            # 最后一个字
            if ind == len(text) - 1:
                line_width.append(sum_width)

        if not paragraph.endswith('\n'):
            paragraph += '[split]'
        return paragraph, line_height, line_count, line_width

    def split_text(self, content):
        # 按规定宽度分组
        max_line_height, total_lines = 0, 0
        max_line_width = 0
        all_line_width = []
        allText = []
        for text in content.split('\n'):
            duanluo, line_height, line_count, line_width = self.get_paragraph(text)
            max_line_height = max(line_height, max_line_height)
            if not line_width:
                line_width.append(0)
            max_line_width = max(max(line_width), max_line_width)  # 记录最长的文本长度
            total_lines += line_count
            all_line_width.extend(line_width)
            allText.append((duanluo, line_count))
        line_height = max_line_height
        total_height = total_lines * line_height

        alltext = [text[0].split('[split]') for text in allText]

        allText = []
        for text in alltext:
            if len(text) == 2 and text[0] == text[1] == '':
                text = [' ']
            allText.extend(text)
            if '' in allText:
                allText.remove('')

        return allText, total_height, line_height, total_lines, max_line_width, all_line_width

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
    def __init__(self, content, loc, font, font_type, fontsize, font_color, input_dir, output_dir, alignment='1'):
        self.content = content
        self.t_top, self.t_left, self.t_width, self.t_height = loc
        self.t_top += 5
        self.t_left += 5
        self.font_type = font_type
        self.font = font
        self.font_size = fontsize
        self.font_color = font_color
        self.intput_dir = input_dir
        self.output_dir = output_dir
        self.alignment = alignment
        self.media_type = 'png' if 'png' in self.output_dir else "mp4"

    def _hex_to_rgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def run(self):
        self._perprocess()

    def _perprocess(self):
        print(f"input_dir: {self.intput_dir}")
        print(f"output_dir: {self.output_dir}")
        text_tools = TextTools(font=os.path.join("../../font_library", self.font[0]), font_size=self.font_size,
                               width=self.t_width)
        allText, total_height, line_height, total_lines, max_line_width, all_line_width = text_tools.split_text(
            self.content)
        line_height_amendment = (self.font_size * 1.15 - line_height) / 2
        # line_height_fixed = self.font_size  # 把一个字当作一个正方形来处理，似乎不行
        line_height_fixed = line_height  # 把一个字当作一个正方形来处理，似乎不行
        allText_length = len(allText)
        if self.alignment == '0':  # 左对齐，直接写不用计算
            self._writer(allText=allText,
                         new_left=self.t_left,
                         new_top=self.t_top + total_height,
                         input_dir=self.intput_dir,
                         output_dir=self.output_dir)
        else:
            stardand_left = self.t_left  # 记录标准坐标
            # stardand_top = self.t_top + line_height
            stardand_top = self.t_top + line_height_fixed + line_height_amendment
            height_record = 0
            ind = 0
            new_top = 0
            base_dir = os.path.split(self.output_dir)[0]
            for text in allText:
                if text == ' ':
                    height_record += line_height
                    ind += 1
                    continue
                _, _, line_height, _, _, all_line_width = text_tools.split_text(text)
                if all_line_width[0] == max_line_width:  # 如果是满行，则直接写
                    new_top = stardand_top + height_record
                    new_left = self._count_offset(text_width=all_line_width,
                                                  max_width=max_line_width,
                                                  alignment=self.alignment) + self.t_left

                    input_dir = os.path.join(base_dir, f'writer_{ind}.' + self.media_type) if ind != 0 else \
                        self.intput_dir
                    output_dir = os.path.join(base_dir, f'writer_{ind + 1}.' + self.media_type) \
                        if ind < allText_length - 1 else self.output_dir
                    self._writer(allText=text,
                                 new_left=new_left,
                                 new_top=new_top,
                                 input_dir=input_dir,
                                 output_dir=output_dir)
                    # height_record += line_height
                    height_record += line_height_fixed + line_height_amendment
                    ind += 1
                else:  # 不是满行需要对齐，因为是当作独立的行来做的，因此只需要计算坐标即可
                    new_top = stardand_top + height_record
                    new_left = self._count_offset(text_width=all_line_width,
                                                  max_width=max_line_width,
                                                  alignment=self.alignment) + self.t_left
                    input_dir = os.path.join(base_dir, f'writer_{ind}.' + self.media_type) if ind != 0 else \
                        self.intput_dir
                    output_dir = os.path.join(base_dir, f'writer_{ind + 1}.' + self.media_type) \
                        if ind < allText_length - 1 else self.output_dir
                    self._writer(allText=text,
                                 new_left=new_left,
                                 new_top=new_top,
                                 input_dir=input_dir,
                                 output_dir=output_dir)
                    ind += 1
                    # height_record += line_height
                    height_record += line_height_fixed + line_height_amendment

    def _writer(self, allText, new_left, new_top, input_dir, output_dir):
        base_dir = os.path.split(output_dir)[0]
        # media_info = ffmpeg.probe(self.intput_dir)['streams'][0]
        media_info = next(
            (stream for stream in ffmpeg.probe(input_dir)['streams'] if stream['codec_type'] == 'video'), None)
        height = media_info['height']
        width = media_info['width']
        text_content = '\###N'.join(text for text in allText) if not isinstance(allText, str) else allText
        text_info = {'content': text_content,
                     'fontsize': self.font_size,
                     'font': self.font[1],
                     'bold': self.font_type[0],
                     'italic': self.font_type[1],
                     'underline': self.font_type[2],
                     'left': new_left,
                     'top': new_top,
                     'color': self.font_color.replace("#", "")}

        # layer_order = os.path.split(self.output_dir)[1].split('_')[0]
        layer_order = '0'
        if self.media_type == 'png':  # 图片直接写即可
            # bkg_info
            bkg_info = {'resolution': [width, height], 'bkg_dir': {self.intput_dir}, 'time': [s2hms(0), s2hms(1)]}
            ass_dir = os.path.join(base_dir, f'{layer_order}_subtitles.ass')
            write_ass(bkg_info=bkg_info, text_info=text_info, output_dir=ass_dir)

            # write
            os.system(
                f"/usr/local/bin/ffmpeg -y -i {input_dir} -vf \"ass={ass_dir}:fontsdir=../../font_library/\" -loglevel error {output_dir}")
            os.system(f"rm -f {ass_dir}")

        else:
            # video_info = ffmpeg.probe(self.intput_dir)['streams'][0]
            video_info = next(
                (stream for stream in ffmpeg.probe(input_dir)['streams'] if stream['codec_type'] == 'video'),
                None)
            out_size = (video_info['width'], video_info['height'])
            video_duration = video_info['duration']

            bkg_info = {'resolution': [width, height], 'bkg_dir': {input_dir},
                        'time': [s2hms(0), s2hms(video_duration)]}
            ass_dir = os.path.join(base_dir, f'{layer_order}_subtitles.ass')
            write_ass(bkg_info=bkg_info, text_info=text_info, output_dir=ass_dir)
            os.system(
                f"/usr/local/bin/ffmpeg -y -i {input_dir} -vf \"ass={ass_dir}:fontsdir=../../font_library/\" -loglevel error {output_dir}")
            os.system(f"rm -f {ass_dir}")

    def _count_offset(self, text_width, max_width, alignment):
        if alignment == '1':  # 居中
            space_text = (self.t_width - max_width) // 2
            return (max_width - text_width[0]) // 2 + space_text
        else:  # 右对齐
            space_text = (self.t_width - max_width)
            return max_width - text_width[0] + space_text


def s2hms(x):  # 把秒转为时分秒
    # x = int(x)
    m, s = divmod(float(x), 60)
    h, m = divmod(m, 60)
    hms = "%01d:%02d:%s" % (h, m, str('%.2f' % s).zfill(5))
    # hms = hms.replace('.', ',')  # 把小数点改为逗号
    return hms


def align_text(text, line_width, text_tools, align):
    all_text = []
    num_text = sum(int(t[1]) for t in text)
    text = [t[0] for t in text]

    for t in text:
        all_text.extend(t.split('[split]'))
        all_text.remove('')
    assert len(all_text) == num_text
    new_text = []  # 记录最后的文本段
    max_width = max(line_width)
    for ind in range(len(line_width)):
        if line_width[ind] != max_width:  # 如果不同则需要补齐长度
            new_content = all_text[ind]
            while True:
                allText, total_height, line_height, total_lines, max_line_width, all_line_width = \
                    text_tools.split_text(new_content)

                if align == 'mid':  # 居中，整体长度为最大值的一半
                    if sum(all_line_width) >= max_width // 2:
                        break
                elif align == 'right':  # 右对齐
                    if sum(all_line_width) >= max_width:
                        break
                new_content = ' ' + new_content
            new_text.append(new_content + '\###N')
        else:
            new_text.append(all_text[ind] + '\###N')

    return new_text


def write_ass(bkg_info, text_info, output_dir):
    """
    :param bkg_info: [bkg_type, bkg_dir, bkg_resolution]
    :param text_info: [content, fontsize, fontcolor, left, top, bold, italic, underline]
    :return:
    """
    bkg_dir = bkg_info['bkg_dir']
    bkg_resolution = bkg_info['resolution']
    bkg_start, bkg_end = bkg_info['time']

    text_content = text_info['content']
    text_font = text_info['font']
    text_color = text_info['color']
    text_fontsize = text_info['fontsize']
    text_bold = text_info['bold']
    text_italic = text_info['italic']
    text_underline = text_info['underline']
    text_left = text_info['left']
    text_top = text_info['top']
    text_bottom = bkg_resolution[1] - text_top

    # res = [1080, 1920]
    info_line1 = f"[Script Info]\n; Script generated by FFmpeg/Lavc58.134.100\nScriptType: v4.00+\n" \
                 f"PlayResX: {bkg_resolution[0]}\nPlayResY: {bkg_resolution[1]}\nScaledBorderAndShadow: no"

    info_line2 = f"[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour," \
                 f"BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle," \
                 f"Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Default,{text_font}," \
                 f"{text_fontsize},&H{text_color},&Hffffff,&H0,&H0,{text_bold},{text_italic},{text_underline}," \
                 f"0,100,100,0,0,1,0,0,0,{text_left},10,{text_bottom},0"

    info_line3 = f"[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n" \
                 fr"Dialogue: 0,{bkg_start},{bkg_end},Default,,0,0,0,,{text_content.replace('###', '')}"

    content = [info_line1 + "\n\n" + info_line2 + "\n\n" + info_line3]
    with open(output_dir, 'w', encoding='utf-8') as f:
        f.writelines(content)


if __name__ == '__main__':
    a = {'fps': 25,
         'stories': [
             {'fps': 25,
              'order': 1,
              'lay_out': {
                  'text': [
                      {'top': 530, 'bold': 'false', 'font': 'simhei', 'left': 322, 'color': '#ffffff', 'width': 500, 'height': 340, 'italic': 'false', 'content': '测试测试测试测试测，试测试测试', 'duration': 5, 'alignment': '0', 'font_size': 18, 'underline': 'false', 'layer_order': 2, 'is_animation': 'false'},
                      {'top': 375, 'bold': 'false', 'font': 'simhei', 'left': 102, 'color': '#ffeb3b', 'width': 100, 'height': 670, 'italic': 'false', 'content': '测试测试测试自动回车1231231231231231222', 'duration': 5, 'alignment': '0', 'font_size': 18, 'underline': 'false', 'layer_order': 9, 'is_animation': 'false'},
                      {'top': 585, 'bold': 'true', 'font': 'simhei', 'left': 865, 'color': '#e5e5e5', 'width': 487, 'height': 365, 'italic': 'true', 'content': '测试测试中对齐中对，齐', 'duration': 5, 'alignment': '1', 'font_size': 18, 'underline': 'true', 'layer_order': 6, 'is_animation': 'false'},
                      {'top': 682, 'bold': 'false', 'font': 'simhei', 'left': 1422, 'color': '#433ecc', 'width': 462, 'height': 347, 'italic': 'false', 'content': '测试测，，试右对齐', 'duration': 5, 'alignment': '2', 'font_size': 24, 'underline': 'false', 'layer_order': 8, 'is_animation': 'false'}], 'charts': [], 'images': [{'top': 0, 'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/bg_import_1652364804024.jpg', 'crop': {}, 'left': 0, 'text': {}, 'width': 1920, 'height': 1080, 'duration': 30, 'layer_order': 0}], 'videos': [], 'persons': [{'id': 'huayuan8_mouth', 'top': 37, 'crop': {'top': 23, 'left': 91, 'width': 524, 'circle': 'true', 'height': 524}, 'left': 10, 'text': {'content': '测试文本'}, 'audio': 'maoxiaomei', 'speed': 1, 'width': 285, 'height': 285, 'duration': 5, 'layer_order': 4}]}, 'batch_no': '996053086667538432'}], 'batch_no': '996053086667538432', 'resolution': '1920*1080', 'video_type': 'mp4', 'time_now': '16_35_5', 'base': '/data/caopei/1-code/0_BGC_chopei/local/996053086667538432'}
    print(3.1 // 2)
    # os.system(f"ffmpeg -i ./data_for_test/white.png -vf scale=1080:1920 ./data_for_test/white_1080_1920.png")
    # {"Mengshen-HanSerif": ["Mengshen-HanSerif.ttf", "Mengshen-Regular"],
    #  "simsun": ["simsun.ttc", "SimSun"],
    #  "宋体": ["simsun.ttc", "SimSun"],
    #  "清松手写体4": ["清松手写体4.ttf", "JasonHandwriting4"],
    #  "jf-openhuninn-1": ["jf-openhuninn-1.0.ttf", "jf-openhuninn-1.0"],
    #  "Mengshen-Handwritten": ["Mengshen-Handwritten.ttf", "Mengshen-Handwritten"],
    #  "素材集市社会体": ["素材集市社会体.otf", "SuCaiJiShi-SheHuiTi"],
    #  "setofont": ["setofont.ttf", "SetoFont"],
    #  "飞花宋体": ["飞花宋体.ttf", "FlyFlowerSong"],
    #  "simhei": ["simhei.ttf", "SimHei"],
    #  "黑体": ["simhei.ttf", "SimHei"],
    #  "BabelStoneHan": ["BabelStoneHan.ttf", "BabelStone Han"],
    #  "Hanzi-Pinyin-Font": ["Hanzi-Pinyin-Font.top.ttf", "Hanzi-Pinyin-Font"],
    #  "SourceHanSerifCN-Regular": ["SourceHanSerifCN-Regular.otf", "Source Han Serif CN"],
    #  "瑞美加张清平硬笔楷书": ["瑞美加张清平硬笔楷书.ttf", "Ramega ZhangQingpingYingbiKaishu"],
    #  "阿朱泡泡体": ["阿朱泡泡体.ttf", "AZPPT_1_1436212_19"],
    #  "逐浪萌芽字": ["逐浪萌芽字.ttf", "ZoomlaMengyas-A080"]}

    TextWriter(content='测试测，，试右对齐',
               # self.t_top, self.t_left, self.t_width, self.t_height
               loc=[682, 1422, 462, 347],
               font=["simhei.ttf", "SimHei"], fontsize=24 * 3,
               font_type='000',
               font_color='#e33b64', input_dir='./data_for_test/white.png',
               output_dir='result/123.png').run()
