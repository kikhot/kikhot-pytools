import fnmatch
import os
import re
import uuid
from datetime import datetime

import requests

import config

# 设置源文件夹和目标文件夹
source_folder = config.source_folder
target_folder = config.img_target_folder


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
def get_relative_path(target, base):
    # 获取绝对路径
    target = os.path.abspath(target)
    base = os.path.abspath(base)

    # 计算相对路径
    relative_path = os.path.relpath(target, base)

    # 计算 `../` 的数量
    num_parents = relative_path.count(os.sep)

    # 返回完整的结果
    return '../' * num_parents + str(relative_path.replace('\\', '/'))


def replace_method():
    # 确保目标文件夹存在
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

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
            # 判断 content 前面是否有 '---' 如果没有，则将 hexo 的文章头信息加入到 content 前面
            if content.startswith('---'):
                pass
            else:
                # 获取 tags 内容，
                tags = pre_path.split('_posts\\')[1].split('\\')
                title = markdown_file.split('\\')[-1].replace('.md', '')
                hexo_head = f'---' \
                            f'\ntitle: {title}' \
                            f'\ndate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' \
                            f'\ntags:' \
                            f'\n  - {'\n  - '.join(tags)}' \
                            f'\ncategories:' \
                            f'\n  - {'\n  - '.join(tags)}' \
                            f'\n---\n'
                hexo_head = hexo_head.format()
                content = hexo_head + content
            # 将<font style="color:rgb(0, 0, 0);"></font>删除
            # 使用正则表达式删除指定的font标签
            content = re.sub(r'<font style="color:rgb\(0, 0, 0\);">(.*?)</font>', r'\1', content)
            # 查找所有匹配的图片URL
            matches = re.findall(image_pattern, content)
            for match in matches:
                # 构建图片的本地文件路径
                image_extension = os.path.splitext(match)[1]
                image_filename = f'image_{uuid.uuid4()}{image_extension}'
                image_path = os.path.join(pre_path.replace('_posts', 'images'), image_filename)
                # 下载图片
                download_image(match, image_path)
                print(f'Downloaded {match} as {image_path}')
                image_counter += 1
                # 将下载的 png 写回 md 中
                img_md = get_relative_path(image_path, source_folder)
                content = content.replace(match, img_md)

            # 将修改后的内容写回文件
            with open(markdown_file, 'w', encoding='utf-8') as f:
                f.write(content)


if __name__ == '__main__':
    replace_method()
