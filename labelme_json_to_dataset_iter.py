'''
批量转换json文件到png文件，对labelme中的json_to_dataset文件的修改
'''
import argparse
import base64
import json
import os
import os.path as osp

import imgviz
import PIL.Image

from labelme.logger import logger
from labelme import utils


def main():
    logger.warning(
        "此脚本旨在演示如何将JSON文件转换为单个图像数据集."
    )
    logger.warning(
        "它将会处理多个 JSON 文件来生成实际使用的数据集."
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("json_file")
    parser.add_argument("-o", "--out", default=None)
    args = parser.parse_args()

    json_file = args.json_file
    print(osp.dirname(json_file))

    if osp.isdir(osp.join(osp.dirname(json_file), 'json_data')) is False:
        os.mkdir(osp.join(osp.dirname(json_file), 'json_data'))
    else:
        print("文件已存在")
    if args.out is None:
        out_dir = osp.basename(json_file).replace(".", "_")
        out_dir1 = osp.join(osp.dirname(json_file), 'json_data')
        out_dir = osp.join(out_dir1, out_dir)
        print(out_dir)
        print("#" * 10)
    else:
        out_dir = args.out
    if not osp.exists(out_dir):
        os.mkdir(out_dir)

    data = json.load(open(json_file))
    imageData = data.get("imageData")

    if not imageData:
        imagePath = os.path.join(os.path.dirname(json_file), data["imagePath"])
        with open(imagePath, "rb") as f:
            imageData = f.read()
            imageData = base64.b64encode(imageData).decode("utf-8")
    img = utils.img_b64_to_arr(imageData)

    label_name_to_value = {"_background_": 0}
    for shape in sorted(data["shapes"], key=lambda x: x["label"]):
        label_name = shape["label"]
        if label_name in label_name_to_value:
            label_value = label_name_to_value[label_name]
        else:
            label_value = len(label_name_to_value)
            label_name_to_value[label_name] = label_value
    lbl, _ = utils.shapes_to_label(
        img.shape, data["shapes"], label_name_to_value
    )

    label_names = [None] * (max(label_name_to_value.values()) + 1)
    for name, value in label_name_to_value.items():
        label_names[value] = name

    lbl_viz = imgviz.label2rgb(
        lbl, imgviz.asgray(img), label_names=label_names, loc="rb"
    )

    PIL.Image.fromarray(img).save(osp.join(out_dir, "img.png"))
    utils.lblsave(osp.join(out_dir, "label.png"), lbl)
    PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir, "label_viz.png"))

    with open(osp.join(out_dir, "label_names.txt"), "w") as f:
        for lbl_name in label_names:
            f.write(lbl_name + "\n")

    logger.info("Saved to: {}".format(out_dir))


if __name__ == "__main__":
    main()