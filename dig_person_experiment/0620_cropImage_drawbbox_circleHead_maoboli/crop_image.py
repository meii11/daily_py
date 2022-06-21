#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/20
"""
# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by MeiiCho on 2022/06/19
"""
import ffmpeg
import os
import cv2


class CropMaterial:
    def preprocess(self, material_type, material_dir, crop_coo, full_coo, output_dir):
        if material_type == 'img':
            self._crop_img(material_dir=material_dir,
                           crop_coo=crop_coo,
                           full_coo=full_coo,
                           output_dir=output_dir)
        elif material_type == 'video':
            self._crop_video(video_dir=material_dir,
                             full_coo=full_coo,
                             output_dir=output_dir)
        else:
            assert Exception("wrong type!")

    def _crop_video(self, video_dir, full_coo, output_dir):

        v_width, v_height, new_top, new_left = self._cal_video_info(video_dir=video_dir,
                                                                    full_coo=full_coo)
        # step1 resize video and output to final output
        base_dir, file_name = os.path.split(output_dir)
        layer_order = file_name.split("_")[0]
        output_dir = os.path.join(base_dir, f"{layer_order}_{int(new_top)}_{int(new_left)}_video.mp4")
        os.system(f"ffmpeg -y -i {video_dir} -vf scale={v_width}:{v_height} -loglevel error {output_dir}")

    def _cal_video_info(self, video_dir, full_coo):
        v_info = ffmpeg.probe(video_dir)['streams'][0]
        v_width, v_height = v_info['width'], v_info['height']

        full_width, full_height = full_coo['width'], full_coo['height']

        ratio = min(full_height / v_height, full_width / v_width)

        v_width = int(v_width * ratio)
        v_height = int(v_height * ratio)
        new_left = int((full_width - v_width) / 2) + full_coo['left']
        new_top = int((full_height - v_height) / 2) + full_coo['top']
        # w_h_ratio = v_width / v_height
        #
        # # 如果高是长边
        # if v_height > v_width:
        #     # 因为视频resize需要偶数边，因此需要做一个判断
        #     v_height = full_height if full_height % 2 == 0 else full_height + 1
        #     v_width = int(w_h_ratio * v_height) if int(w_h_ratio * v_height) % 2 == 0 else int(w_h_ratio * v_height) + 1
        #
        #     new_top = full_coo['top']
        #     new_left = (full_width - v_width) // 2 + full_coo['left']
        # # 宽是长边同理，这里包含了高宽相同的情况
        # else:
        #     v_width = full_width if full_width % 2 == 0 else full_width + 1
        #     v_height = v_width // w_h_ratio if (v_width // w_h_ratio) % 2 == 0 else (v_width // w_h_ratio) + 1
        #
        #     new_top = (full_height - v_height) // 2 + full_coo['top']
        #     new_left = full_coo['left']

        v_width = v_width if v_width % 2 == 0 else v_width + 1
        v_height = v_height if v_height % 2 == 0 else v_height + 1

        return v_width, v_height, new_top, new_left

    def _crop_img(self, material_dir, crop_coo, full_coo, output_dir):
        # 根目录、层级、crop的高宽以及上左距离、resize的
        base_dir, layer_order, c_width, c_height, c_left, c_top, resize_width, resize_height, resize_top, \
        resize_left, tmp_img = \
            self._cal_img_info(material_dir=material_dir,
                               crop_coo=crop_coo,
                               full_coo=full_coo,
                               output_dir=output_dir)
        # step1 crop material
        crop_material = os.path.splitext(tmp_img)[0] + '_resize' + os.path.splitext(tmp_img)[1]
        os.system(
            f"ffmpeg -y -i {tmp_img} -vf crop=w={c_width}:h={c_height}:x={c_left}:y={c_top} -loglevel error "
            f"{crop_material}")

        # step2 resize material
        output_dir = os.path.join(base_dir, f"{layer_order}_{resize_top}_{resize_left}_image.png")
        os.system(
            f"ffmpeg -y -i {crop_material} -vf scale={resize_width}:{resize_height} -loglevel error {output_dir}")

        # os.system(f"rm -f {tmp_img} {crop_material}")

    def _cal_img_info(self, material_dir, crop_coo, full_coo, output_dir):
        base_dir, file_name = os.path.split(output_dir)
        layer_order = file_name.split("_")[0]
        try:
            tmp_img = os.path.join(base_dir, 'crop_negative_coo.png')
            cv2.imwrite(tmp_img, material_dir)
        except:
            tmp_img = material_dir

        m_info = ffmpeg.probe(tmp_img)['streams'][0]
        img_width, img_height = m_info['width'], m_info['height']

        # 计算出抠图部分大小
        if crop_coo['left'] < 0 and crop_coo['top'] >= 0:
            c_left = 0
            c_top = crop_coo['top']

            c_height = min(crop_coo['height'], img_height - crop_coo['top'])
            c_width = min(crop_coo['width'] + crop_coo['left'], img_width)

        # situation 2: left>0 top<0
        elif crop_coo['left'] >= 0 and crop_coo['top'] < 0:
            c_top = 0
            c_left = crop_coo['left']

            c_height = min(crop_coo['height'] + crop_coo['top'], img_height)
            c_width = min(img_width - crop_coo['left'], crop_coo['width'])

        # situation 3: left < 0 top < 0
        elif crop_coo['left'] < 0 and crop_coo['top'] < 0:
            c_top = 0
            c_left = 0

            c_height = min(crop_coo['height'] + crop_coo['top'], img_height)
            c_width = min(crop_coo['width'] + crop_coo['left'], img_width)

        # situation 4: all > 0
        else:
            c_left = crop_coo['left']
            c_top = crop_coo['top']

            c_height = min(crop_coo['height'], img_height - crop_coo['top'])
            c_width = min(crop_coo['width'], img_width - crop_coo['left'])

        full_width, full_height = full_coo['width'], full_coo['height']

        # 图片高宽在剪裁框中的比例
        ratio_height = c_height // crop_coo['height']
        ratio_width = c_width // crop_coo['width']
        # left和top在剪裁框中的比例，因为剪裁框可能超出图片，所以只能计算left和top在剪裁框中的比例，其中当两者大于零是表示比例为0
        ratio_left = abs(crop_coo['left']) // crop_coo['width'] if crop_coo['left'] < 0 else 0
        ratio_top = abs(crop_coo['top']) // crop_coo['height'] if crop_coo['top'] < 0 else 0

        # 这里计算的是剪裁框的相关数据，将剪裁框等比放大或者缩小
        ratio = min(full_height / crop_coo['height'], full_width / crop_coo['width'])
        resize_crop_bound_width = crop_coo['width'] * ratio
        resize_crop_bound_height = crop_coo['height'] * ratio

        # 按照上面的比例计算正确的图像高宽
        resize_img_width = resize_crop_bound_width * ratio_width
        resize_img_height = resize_crop_bound_height * ratio_height

        # step1 计算剪裁框的位置坐标，意思为剪裁框等比放缩后在小背景中的位置坐标
        crop_bound_left = (full_width - resize_crop_bound_width) // 2
        crop_bound_top = (full_height - resize_crop_bound_height) // 2

        # step2 按比例计算剪裁框中图片的位置坐标
        crop_bound_left = crop_bound_left + (resize_crop_bound_width * ratio_left)
        crop_bound_top = crop_bound_top + (resize_crop_bound_height * ratio_top)
        # step3 计算在整个背景上的图片坐标
        crop_bound_left += full_coo['left']
        crop_bound_top += full_coo['top']

        # 用于偶数比例
        resize_img_width = resize_img_width if resize_img_width % 2 == 0 else resize_img_width + 1
        resize_img_height = resize_img_height if resize_img_height % 2 == 0 else resize_img_height + 1

        return base_dir, layer_order, c_width, c_height, c_left, c_top, resize_img_width, resize_img_height, int(
            crop_bound_top), int(crop_bound_left), tmp_img


def main():
    CropMaterial().preprocess(material_type='img',
                              material_dir='./bkg.jpg',
                              crop_coo={'top': -726, 'left': 534, 'width': 3968, 'height': 2806},
                              full_coo={'top': 695, 'left': 1133, 'width': 250, 'height': 100},
                              output_dir='./1_1_1.jpg')
    # os.system(f'ffmpeg -i bg_import_1652364804024.jpg -i 1_720_1187_image.png')

    code = os.system(
        f"ffmpeg -y -threads 6 -i bg_import_1652364804024.jpg -i 1_720_1187_image.png "
        f"-filter_complex 'overlay=1187:720' -loglevel error final.png")
    os.system(f"ffmpeg -y -i final.png -vf 'drawbox=x=1133:y=695:w=248:h=100:color=red@0.5' -loglevel error final11.png")
    os.system(f"ffmpeg -y -i final11.png -vf 'drawbox=x=1128:y=820:w=250:h=100:color=red@0.5' -loglevel error final12.png")
    os.system(f"ffmpeg -y -i final12.png -vf 'drawbox=x=1390:y=210:w=165:h=300:color=red@0.5' -loglevel error final13.png")
    os.system(f"ffmpeg -y -i final13.png -vf 'drawbox=x=553:y=525:w=298:h=300:color=red@0.5' -loglevel error final14.png")

    os.system(f"ffmpeg -y -i final14.png -vf 'drawbox=x=1595:y=210:w=138:h=300:color=red@0.5' -loglevel error final15.png")
    os.system(f"ffmpeg -y -i final15.png -vf 'drawbox=x=1133:y=955:w=250:h=100:color=red@0.5' -loglevel error final16.png")


if __name__ == '__main__':
    main()
    a = 2.1
    b = 2.5
    c = 2.9
    print(round(a), type(round(b)), round(c))
    d = {'top': 695,
         'url': 'https://public-1255423687.cos.ap-shanghai.myqcloud.com/image-ele1655692693026',
         'crop': {'top': -726, 'left': 534, 'width': 3968, 'height': 2806}, 'left': 1133, 'text': {}, 'width': 250,
         'height': 100, 'duration': 5, 'layer_order': 6},
