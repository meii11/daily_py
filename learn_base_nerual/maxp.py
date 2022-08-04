#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/08/03
"""
import torch
import torch.nn as nn


def test_maxpooling():
    features = torch.FloatTensor([
        [1, 2, 6, 7, ],
        [3, 4, 5, 8, ],
        [13, 16, 9, 10, ],
        [14, 15, 12, 11]
    ])
    features.unsqueeze_(0)  # 增加维度
    features.requires_grad_(True)
    pool_data = torch.nn.functional.max_pool2d(features, kernel_size=(2, 2), stride=2)
    print(pool_data)
    # tensor([[[4., 8.],
    #          [16., 12.]]]
    y = torch.sum(pool_data)
    y.backward()
    print(features.grad)
    # tensor([[[0., 0., 0., 0.],
    #          [0., 1., 0., 1.],
    #          [0., 1., 0., 0.],
    #          [0., 0., 1., 0.]]])


if __name__ == '__main__':
    test_maxpooling()
