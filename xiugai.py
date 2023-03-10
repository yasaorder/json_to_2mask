# coding:utf-8

import os
import json

json_dir = 'datasets/zengqiang/silu3/'  # 写入json文件的文件夹路径
json_files = os.listdir(json_dir)

# 写自己的旧标签名和新标签名
old_name = "_background_"
new_name = "background"

for json_file in json_files:
    json_file_ext = os.path.splitext(json_file)

    if json_file_ext[1] == '.json':
        jsonfile = json_dir + json_file

        with open(jsonfile, 'r', encoding='utf-8') as jf:
            info = json.load(jf)

            for i, label in enumerate(info['shapes']):
                if info['shapes'][i]['label'] == old_name:
                    info['shapes'][i]['label'] = new_name
                    # 找到位置进行修改
            # 使用新字典替换修改后的字典
            json_dict = info

        # 将替换后的内容写入原文件
        with open(jsonfile, 'w') as new_jf:
            json.dump(json_dict, new_jf)

print('change name over!')
