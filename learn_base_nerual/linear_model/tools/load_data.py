#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/08/03
"""
import pandas as pd
import numpy as np
from torch.utils.data import Dataset


class LrDataLoader(Dataset):
    def __init__(self, data_tensor, target_tensor):
        super(LrDataLoader, self).__init__()

        self.i_x = data_tensor
        self.i_y = target_tensor

    def __getitem__(self, item):
        return self.i_x[item], self.i_y[item]

    def __len__(self):
        return self.i_y.size(0)


def main():
    data = LrDataLoader()


if __name__ == '__main__':
    main()
