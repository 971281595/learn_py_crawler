# coding:utf-8
import urllib.request
from selenium import webdriver
import re
import json
import os
import timeit


def get_imgs(source_file, base_download_file):
    """参数1 保存URL文件的地址 参数2 保存图片的地址"""
    try:
        os.makedirs(base_download_file)
    except OSError:
        pass
    with open(source_file, 'rb') as f:
        while True:  # 遍历source_file的每一行提取出url和文件名称直到最后一行为止
            # cnt = cnt + 1
            line = f.readline().decode()
            # print(line)
            if line:
                items = line.split(' ')
                #print(items)
                new_items = items[2] + items[1]
                img_id = items[4].split('\n')[0]  # 每张图片的名称
                img_url = items[3]
                file = base_download_file + "\\" + new_items  # 每一话存储的目录
                img_file = file + "\\" + img_id
                if os.path.exists(img_file):  # 如果文件存在跳过此次循环
                    print(img_file, ' exists')
                    continue
                try:     # 尝试下载图片
                    img = urllib.request.urlopen(img_url).read()  # 此函数中这里最花时间
                except:   # 若下载出现错误则记录在指定文件并继续下载
                    with open(base_download_file+'错误记录.txt', 'ab') as error_file:
                        error_file.write(line.encode())     # 记录出现错误的行
                        error_file.write(img_url.encode())  # 记录出现错误的url
                    continue
                try:
                    os.makedirs(file)
                    # print('W:\\爬取一拳超人\\下载结果\\'+new_items)
                except OSError:
                    pass
                with open(img_file, 'wb') as g:
                    g.write(img)
                    print(new_items +" No."+img_id, 'has download')
            else:
                break


if __name__ == '__main__':
    source_file = 'W:\\漫画\\URL\\一拳超人URL.txt'
    base_download_file = 'W:\\漫画\\一拳超人'
    get_imgs(source_file, base_download_file)