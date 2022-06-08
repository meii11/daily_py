#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/05/31
"""
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
def main():
    img = cv2.VideoCapture('./data/video.mp4')
    ret, frame = img.read()
    v_writer = cv2.VideoWriter('./data/2.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25.0, tuple([608, 1080]))
    # note_img = Image.open(Image.fromarray(frame))
    while ret:
        n = Image.fromarray(frame).convert("RGB")
        draw = ImageDraw.Draw(n)

        x, y = 0, 0
        allText = [('小编为a11，,.。大家讲解一下几位抗\n日名将的故事，第一位抗日\n', 2), ('名将杨靖宇，他不仅是白山黑水间的\n铁血将军，也是信念坚定的共产党员。\n他的威名，让敌人闻风丧胆，更令中国\n人骄傲。在1940年初，杨靖宇所带领的\n部队被日军围剿，他们已经断粮五天了\n，他和剩下的十几名战忍妥着饥饿，疲\n劳，与敌人奋战，后来其他战十都牺牲\n了，杨靖宇仍然边战边走。下面讲一讲\n狼牙山五壮士，1941年9月25日，数千名\n日asdasdasd伪军在河北易具狼牙山地区\n实施“清剿”。晋察冀一分区一团七连\n二排六班的5名战士，即班长马宝玉，副\n班长葛振林，战十胡德林、胡福才和宋\n学义，为掩护主力部队和群众转移，与\n敌人激烈战斗，利用有利地形奋勇还击\n，打日伪军多次进攻，毙伤90余人。第\n三个故事是刘胡兰的英雄事迹，1946年1\n2月的一天，刘胡兰配合武工队员将“\n当地一害”石佩怀处死，阎锡山匪军恼\n羞成怒，决定实施报复行动。1947年1月\n12日，阎军突然袭击云周西村，刘胡兰\n因叛徒告密而被捕。刘胡兰烈士牺牲时\n，尚未满15周岁，是已知的中国共产党\n女烈十中年龄最小的一个。毛泽东在指\n挥全国战局之余，为刘胡兰题词:“生的\n伟大，死的光荣!\n', 26)]
        for duanluo, line_count in allText:
            def hex_to_rgb(value):
                value = value.lstrip('#')
                lv = len(value)
                return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
            color = hex_to_rgb("#d53939")
            draw.text((x, y), duanluo, fill=color, font=ImageFont.truetype("./data/simsun.ttc", 30))
            y += 30 * line_count
        n.save('./data/2.png')
        nn = np.array(n)
        v_writer.write(nn)
        ret, frame = img.read()

    v_writer.release()
    return draw

if __name__ == '__main__':
    main()
