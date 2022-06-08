#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/05/29
"""
def _ERROR():
    print('1')
    raise Exception("11")

def main():
    print('2')
    _ERROR()
    print('3')


if __name__ == '__main__':
    main()
