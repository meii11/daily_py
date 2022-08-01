#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/07/29
"""

import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.chrome.options import Options

while 1:
    try:
        s = Service(executable_path='C:\Program Files (x86)\Microsoft\Edge\Application/msedgedriver.exe')
        driver = webdriver.Edge(service=s)
        # driver = webdriver.Edge(executable_path='C:\Program Files (x86)\Microsoft\Edge\Application/msedgedriver.exe')
        # options=webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # driver = webdriver.Chrome(chrome_options=options)

        driver.get('https://login.ecnu.edu.cn/login.ecnu.edu.cn')
        username = driver.find_element_by_name("username")  # 这里别改
        if username.rect['height'] == 0:
            print('Internet is Ok')
            driver.quit()
        else:
            print('Internet is connectting')
            password = driver.find_element_by_name("password")  # 这里别改
            username.send_keys("52173904029")
            password.send_keys("qwe1122")
            loginButton = driver.find_element_by_class_name('btn')
            loginButton.click()
            sleep(10)
            driver.quit()
        sleep(300)
    except:
        print('Error')
        sleep(300)
