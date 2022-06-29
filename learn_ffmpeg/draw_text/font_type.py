#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/29
"""
import os


def main():
    bkg = './bkg.jpg'
    video_bkg = './v_bkg.mp4'
    font = './font/simhei.ttf'
    out = './out.png'
    content = "你好123abc"
    # subtitle
    # os.system(f"ffmpeg -i {bkg} "
    #           f"-lavfi subtitles=subtitles.srt:force_style='Alignment=0,OutlineColour=&H100000000,BorderStyle=3,"
    #           f"Outline=1,Shadow=0,Fontsize=18,MarginL=5,MarginV=25'-crf 1 -c:a copy {out}")
    os.system(f"ffmpeg -y -i {video_bkg} ass=2.ass output.mp4")
    # code = os.system( f"ffmpeg -y -threads 10 -i {bkg} -vf 'drawtext=text={content}:expansion=normal:fontfile={
    # font}:y={0}:x={0}:" f"fontcolor=white:fontsize=300:Bold=0' -loglevel error {out}")


def s2hms(x):  # 把秒转为时分秒
    m, s = divmod(x, 60)
    h, m = divmod(m, 60)
    hms = "%02d:%02d:%s" % (h, m, str('%.3f' % s).zfill(6))
    hms = hms.replace('.', ',')  # 把小数点改为逗号
    return hms


# with open('字幕文件.srt', 'w', encoding='utf-8') as f:
#     write_content = [str(n + 1) + '\n' + s2hms(i['from']) + ' --> ' + s2hms(i['to']) + '\n' + i['content'] + '\n\n' for
#                      n, i in enumerate(sub_content)]  # 序号+开始-->结束+内容
#     f.writelines(write_content)

if __name__ == '__main__':
    # main()

    print(s2hms(110))