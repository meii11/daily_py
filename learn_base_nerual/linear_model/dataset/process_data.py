#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/08/03
"""
import numpy as np
import pandas as pd


def main():
    func = lambda x: 2 * x + 3 + np.random.randint(-100, 100, 1)

    i_x = np.arange(1, 500, 2)
    i_y = func(i_x)

    i_data = pd.DataFrame({'i_x': i_x, 'i_y': i_y})
    i_data.to_csv("data.csv")
    # print(i_x)
    print(i_data)


if __name__ == '__main__':
    main()
