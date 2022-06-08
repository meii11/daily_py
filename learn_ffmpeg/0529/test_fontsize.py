#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/05/29
"""
import os
import subprocess

def main():
    # 将图片标准化为30 30
    # os.system("ffmpeg -y -i ./data/kaori.jpeg -vf scale=80:80 out.png")

    # 写入一个字号30的字
    input_png = './data/bg.jpg'
    # content = "刘胡兰（1932年10月8日—1947年1月12日），女，汉族， [1]  原名刘富兰 [7]  ，山西省吕梁市文水县云周西村人。著名的革命先烈，;:优秀共产党员。"\ .replace(",",
    # "\\\\\\,").replace("]", "\\\\\\]").replace("[", "\\\\\\[").replace(";", "\\\\\\;").\ replace(":",
    # "\\\\\\:").replace("<", "\\\\\\<").replace(">", "\\\\\\>").replace("?", "\\\\\\?").replace(".", "\\\\\\.")

    content = "'jj'"
    font_type = './data/simhei.ttf'
    font_size = 13 * 3
    # font_size = font_size * 2.83 / 72 * 96 os.system("ffmpeg -i ./data/front.png -vf crop=w=1288:h=511:x=0:y=18
    # ./data/crop_front.png") code = os.system( f"ffmpeg -y -i {input_png} " f"-vf 'drawtext=text={
    # content}:expansion=normal:fontfile={font_type}:y=(h-text_h)/2:x=(w-text_w)/2:fontcolor=black:fontsize={
    # font_size}' " f"-loglevel error 30_en.png") os.system( "ffmpeg -i ./data/bg.jpg -i ./data/crop_front.png
    # -filter_complex '[0:v]scale=1080:1920[bg];[1:v]scale=1070:425[front];[bg][front]overlay=0:0' "
    # "./data/overlay.png")

    # code = os.system( f"ffmpeg -y -i ./data/overlay.png " f"-vf 'drawtext=text={
    # content}:expansion=normal:fontfile={font_type}:y=(h-text_h)/2:x=(w-text_w)/2:fontcolor=black:fontsize={
    # font_size}' " f"-loglevel error 30_en.png")
    sub = "(930-text_w)/2+70"
    subprocess.call(['ffmpeg', '-y', '-i', './data/overlay.png', '-vf', 'drawtext=text=', content,
                     ':expansion=normal:fontfile=', font_type, ':y=', '437', ':x=', '930', ':fontcolor=black:fontsize=',
                     '39', '30_en.png'])
    # code = os.system(
    #     f"ffmpeg -y -i ./data/overlay.png "
    #     f"-vf 'drawtext=text={content}:expansion=normal:fontfile={font_type}:y={437}:x=({930}-text_w)/2+{70}:fontcolor=black:fontsize={font_size}' "
    #     f"-loglevel error 30_en.png")


if __name__ == '__main__':
    main()
    data = {"fps": 30,
            "stories": [
                {"fps": 30,
                 "order": 1,
                 "lay_out":
                     {"text":
                         [
                             {"top": 65, "font": "黑体", "left": 87, "color": "#000000", "width": 542, "height": 250,
                              "content": "小编为大家讲解一下几位抗日名将的故事，第一位抗日名将杨靖宇，他不仅是白山黑水间的铁血将军，也是信念坚定的共产党员。他的威名，让敌人闻风丧胆，更令中国人骄傲。在1940年初，杨靖宇所带领的部队被日军围剿，他们已经断粮五天了，他和剩下的十几名战忍妥着饥饿，疲劳，与敌人奋战，后来其他战十都牺牲了，杨靖宇仍然边战边走。",
                              "duration": 5, "font_size": 36, "layer_order": 2,
                              "is_animation": "false"},
                             {"top": 1252, "font": "黑体", "left": 70, "color": "#000000", "width": 922, "height": 630,
                              "content": "bbb", "duration": 5, "font_size": 13, "layer_order": 7,
                              "is_animation": "false"},
                             {"top": 610, "font": "黑体", "left": 72, "color": "#000000", "width": 922, "height": 572,
                              "content": "aaa", "duration": 5, "font_size": 13, "layer_order": 6,
                              "is_animation": "false"},
                             {"top": 437, "font": "黑体", "left": 70, "color": "#000000", "width": 930, "height": 115,
                              "content": "咩咩咩", "duration": 5, "font_size": 13, "layer_order": 5,
                              "is_animation": "false"}], "charts": [],
                         "images": [{"top": 0,
                                     "url": "https://public-1255423687.cos.ap-shanghai.myqcloud.com/bg_import_1652363671114.jpg",
                                     "crop": {}, "left": 0, "text": {}, "width": 1080, "height": 1920, "duration": 30,
                                     "layer_order": 0},
                                    {"top": 0,
                                     "url": "https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1653615661365",
                                     "crop": {"top": 18, "left": 0, "width": 1288, "height": 511},
                                     "left": 0, "text": {}, "width": 1070, "height": 425, "duration": 5,
                                     "layer_order": 1}], "videos": [], "persons": [
                         {"id": "007black", "top": 70, "crop": {"top": 97, "left": 250, "width": 358, "height": 358},
                          "left": 730, "text": {"content": "测试一下是否能够生成成功。"}, "audio": "xiaoxian", "speed": 1,
                          "width": 235, "height": 235, "duration": 5, "layer_order": 4}]},
                 "batch_no": "979683304879947776"}], "batch_no": "979683304879947776", "resolution": "1080*1920",
            "video_type": "mp4"}
