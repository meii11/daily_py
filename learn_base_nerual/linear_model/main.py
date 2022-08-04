#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/08/03
"""
import torch

from model import Lr
from tools.load_data import LrDataLoader
from torch import optim
import torch.nn as nn
from torch.utils.data import DataLoader
import pandas as pd

from matplotlib import pyplot as plt


def main():
    print("===> Simply Linear Model")

    print("===> Load data")
    data_dir = './dataset/data.csv'
    data = pd.read_csv(data_dir)
    data_tensor = torch.Tensor(data['i_x']).resize(250, 1)
    target_tensor = torch.Tensor(data['i_y']).resize(250, 1)
    train_dataLoader = DataLoader(LrDataLoader(data_tensor, target_tensor), batch_size=10)
    model = Lr()
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.00001)

    for ind in range(50000):
        for data in train_dataLoader:
            out = model.forward(data[0])

            loss = criterion(data[1], out)  # 3.2 计算损失

            optimizer.zero_grad()  # 3.3 梯度归零
            loss.backward()  # 3.4 计算梯度
            optimizer.step()  # 3.5 更新梯度

        print('Epoch[{}/{}], loss: {:.6f}'.format(ind, 50000, loss.data))

    model.eval()
    predict = model(data_tensor)
    predict = predict.cpu().detach().numpy()  # 转化为numpy数组
    plt.scatter(data_tensor.cpu().data.numpy(), target_tensor.cpu().data.numpy(), c="r", s=1)
    plt.plot(data_tensor.cpu().data.numpy(), predict)
    plt.show()

    print(model.state_dict().keys())

    torch.save(model.state_dict(), "./pretrained/model_parameter.pkl")


if __name__ == '__main__':
    main()
