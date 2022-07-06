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

            width, height = draw.textsize(text[ind], self.font)
            sum_width += width
            paragraph += text[ind]
            line_height = max(height, line_height)
            if ind < len(text) - 1:
                next_width, _ = draw.textsize(text[ind + 1], self.font)
            else:
                next_width = 0  # 最后一个字了
            if sum_width + next_width > self.width:  # 超过预设宽度就修改段落 以及当前行数
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
            max_line_width = max(max(line_width), max_line_width)  # 记录最长的文本长度
            total_lines += line_count
            all_line_width.extend(line_width)
            allText.append((duanluo, line_count))
        line_height = max_line_height
        total_height = total_lines * line_height

        alltext = [text[0].split('[split]') for text in allText]

        allText = []
        for text in alltext:
            allText.extend(text)
            allText.remove("")

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
    def __init__(self, content, loc, font, font_type, fontsize, font_color, input_dir, output_dir, alignment='0'):
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
        text_tools = TextTools(font=os.path.join("./font_library", self.font[0]), font_size=self.font_size,
                               width=self.t_width)
        allText, total_height, line_height, total_lines, max_line_width, all_line_width = text_tools.split_text(
            self.content)
        allText_length = len(allText)
        if self.alignment == '0':  # 左对齐，直接写不用计算
            self._writer(allText=allText,
                         new_left=self.t_left,
                         new_top=self.t_top + total_height,
                         input_dir=self.intput_dir,
                         output_dir=self.output_dir)
        else:
            stardand_left = self.t_left  # 记录标准坐标
            stardand_top = self.t_top + line_height
            height_record = 0
            ind = 0
            new_top = 0
            base_dir = os.path.split(self.output_dir)[0]
            for text in allText:
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
                    height_record += line_height
                    ind += 1
                else:  # 不是满行需要对齐，因为是当作独立的行来做的，因此只需要计算坐标即可
                    new_top = stardand_top + height_record
                    new_left = self._count_offset(text_width=all_line_width,
                                                  max_width=max_line_width,
                                                  alignment=self.alignment) + self.t_left
                    input_dir = os.path.join(base_dir, f'writer_{ind}.' + self.media_type) if ind != 0 else \
                        self.intput_dir
                    output_dir = os.path.join(base_dir, f'writer_{ind+1}.'+self.media_type) \
                        if ind < allText_length-1 else self.output_dir
                    self._writer(allText=text,
                                 new_left=new_left,
                                 new_top=new_top,
                                 input_dir=input_dir,
                                 output_dir=output_dir)
                    ind += 1
                    height_record += line_height

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
                f"/usr/local/bin/ffmpeg -y -i {input_dir} -vf \"ass={ass_dir}:fontsdir=./font_library/\" -loglevel error {output_dir}")
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
                f"/usr/local/bin/ffmpeg -y -i {input_dir} -vf \"ass={ass_dir}:fontsdir=./font/\" -loglevel error {output_dir}")
            os.system(f"rm -f {ass_dir}")

        os.system(
            f"ffmpeg -y -i {self.output_dir} -vf 'drawbox=x={self.t_left}:y={self.t_top}:w={self.t_width}:h={self.t_height}:color=black' -loglevel error "
            f"./data_for_test/ff.png")
        os.system(
            f"ffmpeg -y -i ./data_for_test/ff.png -vf 'drawbox=x={self.t_left}:y={self.t_top}:w={self.t_width // 2}:h={self.t_height}:color=black' -loglevel error "
            f"./data_for_test/fff.png")

    def _count_offset(self, text_width, max_width, alignment):
        if alignment == '1':  # 居中
            space_text = (self.t_width - max_width) // 2
            return (max_width-text_width[0])//2 + space_text
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
    a = {'top': 1025,
         'font': '黑体',
         'left': 53,
         'color': '#ffffff',
         'width': 760,
         'height': 165,
         'content': '生态奇妙屋：\n汇聚了来自不同地域的植物标本',
         'duration': 5,
         'font_size': 14, 'layer_order': 2, 'is_animation': 'false', 'bold': 'true', 'italic': 'true',
         'underline': 'true'},
    # white_bkg = np.full((1080,1920,3), 255)
    # cv2.imwrite('white.png', white_bkg)
    TextWriter(content='你好你好你好你好你好你\n好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好',
               # self.t_top, self.t_left, self.t_width, self.t_height
               loc=[363, 843, 428, 228],
               font=['simhei.ttf', 'SimHei'], fontsize=14 * 3,
               font_type='000',
               font_color='#000000', input_dir='./data_for_test/white.png',
               output_dir='./data_for_test/test.png').run()

    """
    {'top': 363, 'font': '黑体', 'left': 843, 'color': '#000000', 'width': 428, 'height': 228,
                  'content': '你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你好你',
                  'duration': 5, 'font_size': 14, 'layer_order': 7, 'is_animation': 'false'}
    """
