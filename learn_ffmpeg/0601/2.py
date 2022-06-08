#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/01
"""
from add_Text import TextWriter
import os


def main():
    # os.system("ffmpeg -y -i ./data/bg.jpg -vf scale=1920:1080 ./new_bg.png")
    # img = './new_bg.png'
    # # t_top, t_left, t_width, t_height
    # TextWriter(content="红色故事分享", loc=[375, 102, 100, 670], font_type='./data/simsun.ttc', fontsize=36,
    #            font_color='#ff0000', input_dir=img, output_dir='./data/add1.png').run()

    # TextWriter(content="八路军晋察冀军区第1军分区1团7连6班 ，为在河北省保定市易县狼牙山战斗中英勇抗击日军和伪满洲国军的八路军5位英雄，他们是马宝玉、葛振林、宋学义、胡德林、胡福才",
    #            loc=[585, 865, 487, 365], font_type='./data/simsun.ttc', fontsize=36,
    #            font_color='#ff0000', input_dir='./data/add1.png', output_dir='./data/add2.png').run()

    # TextWriter(content="刘胡兰（1932年10月8日—1947年1月12日），女，汉族， [1]  原名刘富兰 [7]  ，山西省吕梁市文水县云周西村人。著名的革命先烈，优秀共产党员。",
    #            loc=[682, 1422, 462, 347], font_type='./data/simsun.ttc', fontsize=36,
    #            font_color='#ff0000', input_dir='./data/add2.png', output_dir='./data/add3.png').run()

    TextWriter(content="杨靖宇1905年2月-1940年2月23日，男，汉族  ，中国共产党优秀党员，无产阶级革命家、军事家、著名抗日民族英雄，鄂豫皖苏区及其红军的创始人",
               loc=[530, 322, 500, 340], font_type='./data/simsun.ttc', fontsize=36,
               font_color='#ff0000', input_dir='./data/add3.png', output_dir='./data/add4.png').run()
    color = '#ff0000'
    # a = tuple(int(color[i:i + 6 // 3], 16) for i in range(0, lv, lv // 3))
    color = color.split("#")[1]
    c = [#0000ff]
    aa = [color[i:i + 2] for i in range(0, len(color), 2)]
    aa[0],aa[2] = aa[2], aa[0]

    aa = ''.join(aa)
    pass
if __name__ == '__main__':
    main()
    # {'top': 375, 'font': '黑体', 'left': 102, 'color': '#ff0000', 'width': 100, 'height': 670, 'content': '红色故事分享',
    #  'duration': 5, 'font_size': 13, 'layer_order': 9, 'is_animation': 'false'},
    # {'top': 585, 'font': '黑体', 'left': 865, 'color': '#ff0000', 'width': 487, 'height': 365,
    #  'content': '八路军晋察冀军区第1军分区1团7连6班 ，为在河北省保定市易县狼牙山战斗中英勇抗击日军和伪满洲国军的八路军5位英雄，他们是马宝玉、葛振林、宋学义、胡德林、胡福才', 'duration': 5,
    #  'font_size': 13, 'layer_order': 6, 'is_animation': 'false'},
    # {'top': 682, 'font': '黑体', 'left': 1422, 'color': '#ff0000', 'width': 462, 'height': 347,
    #  'content': '刘胡兰（1932年10月8日—1947年1月12日），女，汉族， [1]  原名刘富兰 [7]  ，山西省吕梁市文水县云周西村人。著名的革命先烈，优秀共产党员。', 'duration': 5,
    #  'font_size': 13, 'layer_order': 8, 'is_animation': 'false'},
    # {'top': 530, 'font': '黑体', 'left': 322, 'color': '#ff0000', 'width': 500, 'height': 340,
    #  'content': '杨靖宇1905年2月-1940年2月23日，男，汉族  ，中国共产党优秀党员，无产阶级革命家、军事家、著名抗日民族英雄，鄂豫皖苏区及其红军的创始人', 'duration': 5,
    #  'font_size': 13, 'layer_order': 2, 'is_animation': 'false'}
