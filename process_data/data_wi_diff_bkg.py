#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/07/18
"""
import glob
import json
import os.path

import cv2
import numpy as np

from tqdm import tqdm


def main():
    # resize()

    image_dir = '../../PhotoMatte85_reshape_original'
    """
    1. 构建alpha通道图
    2. 给每张图像添加纯绿色背景以及渐变白色背景（取最高值白色到最低值白色）
    2.5 打包
    3. 按照25帧标准随机重复5-10s当作视频处理
    """
    img_list = glob.glob(f"{image_dir}/*png")
    bkg_dir = '../../diff_bkg'
    bkg_name = [['female_red.mp4', 2], ['man_black.mp4', 2], ['male_sit.mp4', 1], ['female_witable.mp4', 1]]
    # for img in tqdm(img_list):
    #     get_alpha(img)
    #     img_dir, img = os.path.split(img)
    #     img_name, img_type = os.path.splitext(img)

    for bkg in bkg_name:
        _get_diff_bkg(video=os.path.join(bkg_dir, bkg[0]), tag=bkg[1])

    # for img in tqdm(img_list):
    #     overlay(img)

    # 打包之前的文件
    package()

    # 产生随机数
    re = list(np.random.randint(1, 3, [340]))
    f = open('./random_arr.txt', 'w')
    f.write(str(re))
    f.close()
    frame_repeat()
    check()
    # pass


def resize():
    image_dir = '../../PhotoMatte85_original'

    files = glob.glob(f"{image_dir}/*png")

    for file in files:
        out_dir = '../../PhotoMatte85_reshape_original'
        output = os.path.split(file)

        output_dir = os.path.join(out_dir, output[1])
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        os.system(f"ffmpeg -y -i {file} -vf scale=768:-1,crop=768:1080:0:72 -loglevel error {output_dir}")


def check():
    target_train_dir = '../../unidt_dataset_chomeii/train'

    target_train_dir_fgr_bkg = os.path.join(target_train_dir, 'fgr_bkg')
    target_train_dir_fgr = os.path.join(target_train_dir, 'fgr')
    target_train_dir_pha = os.path.join(target_train_dir, 'pha')

    random_repeat_list = eval(open('./random_arr.txt', 'r').readline())
    ind = 0

    for _, dirs, _ in os.walk(target_train_dir_fgr_bkg):
        for _dir in tqdm(dirs):
            fgr = os.path.join(target_train_dir_fgr, _dir)
            fgr_bkg = os.path.join(target_train_dir_fgr_bkg, _dir)
            pha = os.path.join(target_train_dir_pha, _dir)

            assert len(glob.glob(f"{fgr}/*png")) == len(glob.glob(f"{fgr_bkg}/*png")) == len(glob.glob(f"{pha}/*png")), \
                f"长度不相同！{_dir}"

            assert len(glob.glob(f"{fgr}/*png")) == random_repeat_list[ind] * 25, f"长度不相同！{_dir}"
            ind += 1


def package():
    img_alpha_dir = '../../PhotoMatte85_reshape'
    img_wi_bkg_dir = '../../PhotoMatte85_reshape_original_wi_bkg'
    bkg_dir = '../../diff_bkg'

    target_train_dir = '../../unidt_dataset_chomeii/train'

    if not os.path.exists(target_train_dir):
        os.makedirs(target_train_dir)

    img_wi_bkg_list = glob.glob(f"{img_wi_bkg_dir}/*png")

    for img_wi_bkg in tqdm(img_wi_bkg_list):
        img_dir, img_name = os.path.split(img_wi_bkg)
        img_name, img_type = os.path.splitext(img_name)
        true_img_name, bkg_type = '_'.join(img_name.split("_")[:-2]), '_'.join(img_name.split("_")[-2:])

        img_alpha = glob.glob(f"{os.path.join(img_alpha_dir, true_img_name)}/*alpha*")[0]

        bkg = os.path.join(bkg_dir, bkg_type + '.png')

        target_train_dir_fgr_bkg = os.path.join(target_train_dir, 'fgr_bkg', img_name)
        target_train_dir_fgr = os.path.join(target_train_dir, 'fgr', img_name)
        target_train_dir_pha = os.path.join(target_train_dir, 'pha', img_name)

        if not os.path.exists(target_train_dir_fgr_bkg):
            os.makedirs(target_train_dir_fgr_bkg)
            os.makedirs(target_train_dir_fgr)
            os.makedirs(target_train_dir_pha)

        os.system(f"cp {img_alpha} {target_train_dir_pha}")
        os.system(f"cp {bkg} {target_train_dir_fgr_bkg}")
        os.system(f"cp {img_wi_bkg} {target_train_dir_fgr}")


def frame_repeat():
    random_repeat_list = eval(open('./random_arr.txt', 'r').readline())

    fgr_dir = '../../unidt_dataset_chomeii/train/fgr'
    fgr_bkg_dir = '../../unidt_dataset_chomeii/train/fgr_bkg'
    pha_dir = '../../unidt_dataset_chomeii/train/pha'
    ind = 0
    for _, dirs, _ in os.walk(fgr_dir):
        for dir in tqdm(dirs):
            fgr_bkg = os.path.join(fgr_bkg_dir, dir)
            fgr = os.path.join(fgr_dir, dir)
            pha = os.path.join(pha_dir, dir)
            do_repeat(fgr_bkg, random_repeat_list[ind])
            do_repeat(fgr, random_repeat_list[ind])
            do_repeat(pha, random_repeat_list[ind])
            ind += 1


def do_repeat(img_dir, repeat_times):
    img = glob.glob(f"{img_dir}/*")[0]
    img_d = os.path.split(img)[0]
    for i in range(25 * repeat_times):
        os.system(f"cp {img} {os.path.join(img_d, '%06d.png' % i)}")

    os.system(f'rm -f {img}')


def get_alpha(image):
    img_dir, img = os.path.split(image)
    img_name, img_type = os.path.splitext(img)

    img_info = cv2.imread(image, cv2.IMREAD_UNCHANGED)
    alpha = img_info[:, :, 3]

    height, width = img_info.shape[:2]
    # True表示扣掉，False表示不抠
    mask = alpha != 0
    grey_img = np.full((height, width), 255.0) * mask

    alpha_out_dir = os.path.join(img_dir, img_name, img_name + "_alpha" + img_type)
    if not os.path.exists(os.path.join(img_dir, img_name)):
        os.makedirs(os.path.join(img_dir, img_name))
    cv2.imwrite(alpha_out_dir, grey_img)
    os.system(f"mv {image} {os.path.join(img_dir, img_name)}")


def _get_diff_bkg(video, tag):
    """
    :param video: input video with different background
    :param tag: 1 -> pure white or green
                2 -> gradual change white or green
    :return: None
    """
    video_reader = cv2.VideoCapture(video)
    ret, frame = video_reader.read()
    v_frame_width = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
    v_frame_height = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
    outdir = os.path.split(video)[0]

    if ret:
        if tag == 1:
            # 纯色只需要取左上角的颜色即可
            # pure_bkg = np.zeros_like(frame)
            # tmp_frame = cv2.VideoCapture(video).read()
            pure_bkg = np.zeros((v_frame_height, v_frame_width, 3), np.uint8)

            pixel = frame[0][0]
            pure_bkg[:, :, :] = pixel

            output_dir = os.path.join(outdir, 'pure.png')
            if os.path.isfile(output_dir):
                output_dir = os.path.join(outdir, 'pure_0.png')

            # cv2.imwrite(output_dir, pure_bkg)
            tmp = './tmp.png'
            cv2.imwrite(output_dir, pure_bkg)
            # os.system(f"ffmpeg -y -i {tmp} -vf scale=2304:3456 {output_dir}")
            # os.system(f"rm -f {tmp}")
        elif tag == 2:
            # pixel_left_top_corner = frame[0][0]
            # pixel_left_bottom_corner = frame[-1][0]
            # pixel_right_top_corner = frame[0][-1]
            # pixel_right_bottom_corner = frame[-1][-1]
            pixel_final = np.zeros((v_frame_height, v_frame_width, 3), np.uint8)
            for color in range(3):
                pixel = frame[:, :, color]
                pixel_left = pixel[:, 0]
                pixel_right = pixel[:, -1]

                # change_range = 768

                for ind in range(1080):
                    pixel_line = np.linspace(pixel_left[ind], pixel_right[ind], 768)
                    pixel_final[ind, :, color] = pixel_line
            tmp = './tmp.png'
            output_dir = os.path.join(outdir, 'gradual.png')
            if os.path.isfile(output_dir):
                output_dir = os.path.join(outdir, 'gradual_0.png')

            cv2.imwrite(output_dir, pixel_final)
            # os.system(f"ffmpeg -y -i {tmp} -vf scale=2304:3456 {output_dir}")
            # os.system(f"rm -f {tmp}")
    # video_reader.release()


def overlay(image):
    img_dir, img = os.path.split(image)
    img_name, img_type = os.path.splitext(img)

    white_pure = '../../diff_bkg/white_pure.png'
    white_gradual = '../../diff_bkg/white_gradual.png'
    green_pure = '../../diff_bkg/green_pure.png'
    green_gradual = '../../diff_bkg/green_gradual.png'

    bkgs = [white_pure, white_gradual, green_pure, green_gradual]

    for bkg in bkgs:

        output_name = os.path.join(img_dir + "_wi_bkg", img_name + f"_{os.path.split(bkg)[1].split('.')[0]}.png")
        if not os.path.exists(img_dir + "_wi_bkg"):
            os.makedirs(img_dir + "_wi_bkg")

        os.system(f"ffmpeg -y -i {bkg} -i {image} -filter_complex overlay=0:0 -loglevel error {output_name}")


if __name__ == '__main__':
    main()
