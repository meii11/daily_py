#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/30
"""


def main():
    # a = r'你好\[abs]n你好\[abs]n你好'
    #
    # b = a.replace("[abs]n", 'N')
    #
    # print(b)
    s2hms(10)


def s2hms(x):  # 把秒转为时分秒
    m, s = divmod(x, 60)
    h, m = divmod(m, 60)
    hms = "%01d:%02d:%s" % (h, m, str('%.2f' % s).zfill(5))
    hms = hms.replace('.', ',')  # 把小数点改为逗号
    return hms


if __name__ == '__main__':
    main()
