#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/07/06
"""
import json

import PIL
from PIL import ImageFont
import os


def main():
    # PIL.ImageFont.truetype(font=None, size=10, index=0, encoding=”)
    font = './font_library/阿朱泡泡体.ttf'
    a = PIL.ImageFont.truetype(font=font, size=10, index=0)
    print(a.font.family)
    # # pass
    # font_name = {}
    # for _, _, files in os.walk('../../font_library'):
    #     for file_name in files:
    #         if file_name == '.DS_Store':
    #             continue
    #
    #         base_dir = '../../font_library'
    #         font_file = os.path.join(base_dir, file_name)

            # family_name = PIL.ImageFont.truetype(font=font_file, size=10, index=0).font.family
            # with open('./font_pair.txt', 'a') as f:
            #     f.write(f"{file_name} -- {family_name}\n")
            # font_name[file_name] = family_name

    # with open('./font_list.txt', 'w') as f:
    #     f.write(json.dumps(font_name, ensure_ascii=False))


if __name__ == '__main__':
    main()
