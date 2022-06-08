#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/05/15
"""
import face_recognition


def main():
    image = face_recognition.load_image_file("1.png")
    face_landmarks_list = face_recognition.face_landmarks(image)


if __name__ == '__main__':
    main()
