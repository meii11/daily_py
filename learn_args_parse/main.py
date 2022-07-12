#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/07/12
"""
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--batch-size', type=str, default=123)

def main():
    args = parser.parse_args()
    print(args.batch_size)


if __name__ == '__main__':
    main()
