import fnmatch
import os
import re
import uuid

import requests

import config

# 设置源文件夹和目标文件夹
source_folder = config.source_folder


# 定义一个函数来下载图片
def download_image(url, file_path):
    response = requests.get(url)
    # 假设image_path是完整的文件路径，包括文件名
    directory = os.path.dirname(file_path)

    # 检查目录是否存在，如果不存在则创建
    if not os.path.exists(directory):
        os.makedirs(directory)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)


# 将 md 中的 url 变成 ../../ 这种结构
def get_relative_path(img_name):
    # 返回完整的结果
    return './image/' + img_name


def replace_method():
    # 遍历源文件夹中的所有.md文件
    markdown_files = {}
    for root, dirs, filenames in os.walk(source_folder):
        for filename in fnmatch.filter(filenames, '*.md'):
            markdown_files[os.path.join(root, filename)] = root

    # 图片编号
    image_counter = 1

    # 正则表达式来匹配图片URL
    image_pattern = re.compile(r'!\[.*?\]\((https://cdn.nlark.com/.*?)\)')

    # 遍历所有.md文件
    for markdown_file, pre_path in markdown_files.items():
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()

            # 将<font style="color:rgb(0, 0, 0);"></font>删除
            # 使用正则表达式删除指定的font标签
            content = re.sub(r'<font style="color:rgb\(0, 0, 0\);">(.*?)</font>', r'\1', content)
            content = re.sub(r'<font style="color:rgb\(255, 0, 1\);">(.*?)</font>', r'\1', content)

            # 查找所有匹配的图片URL
            matches = re.findall(image_pattern, content)
            for match in matches:
                # 构建图片的本地文件路径
                image_extension = os.path.splitext(match)[1]
                image_filename = f'image_{uuid.uuid4()}{image_extension}'
                image_path = os.path.join(pre_path + '\\image', image_filename)
                # 下载图片
                download_image(match, image_path)
                print(f'Downloaded {match} as {image_path}')
                image_counter += 1
                # 将下载的 png 写回 md 中
                img_md = get_relative_path(image_filename)
                content = content.replace(match, img_md)

            # 将修改后的内容写回文件
            with open(markdown_file, 'w', encoding='utf-8') as f:
                f.write(content)


if __name__ == '__main__':
    replace_method()
