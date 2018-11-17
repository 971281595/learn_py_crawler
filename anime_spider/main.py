# coding:utf-8
import urllib.request
from selenium import webdriver
import re
import json
import os
import timeit
from get_total_url import get_all_url
from get_imgs_url import get_all_img_url
from get_imgs import get_imgs
# 计时开始
time1 = timeit.default_timer()
# 下载每一话的URL
name = '一拳超人'
url = 'https://www.ishuhui.com/comics/anime/53'   # 对应漫画主页URL
pattern = r'(comics.detail.(.*?))"'
filename = 'W:\\漫画\\尾缀\\'+name+'.txt'
num_filename = get_all_url(url, pattern, filename)
# 下载所有图片的URL
base_url = 'https://prod-api.ishuhui.com/comics/detail?id={}'
download_filename = 'W:\\漫画\\URL\\'+name+'URL.txt'
source_file = get_all_img_url(base_url, download_filename, num_filename)
# 下载所有图片
base_download_file = 'W:\\漫画\\'+name
get_imgs(source_file, base_download_file)
# 计时结束
time2 = timeit.default_timer()
print('the download took %d s' % (time2-time1))