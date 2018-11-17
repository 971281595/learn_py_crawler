# coding:utf-8
import urllib.request
from selenium import webdriver
import re
import json
import os
import timeit


def get_num(filename):          #  获取每一话的url尾缀的集合
    with open(filename, 'rb') as f:
        res = f.read().decode()
    ans = res.split('\n')
    return ans

def get_all_img_url(base_url, download_filename, num_filename):
    """参数1 存储json格式数据的URL 参数2 所有图片URL的保存地址 参数3 保存每一话URL的文件地址"""
    num_set = get_num(num_filename)   # 获取每一话的url尾缀的集合
    cnt = 0
    for i in num_set:
        if i == "":     # 最后一个""直接退出
            break
        url = base_url.format(i)  # 获取一话的url
        imgs = urllib.request.urlopen(url)  # 获取对应url数据
        tmp_dict = json.loads(imgs.read())  # 将获取的json格式数据转化成python对应的数据类型
        # print(tmp_dict)
        data = tmp_dict['data']             # 获取漫画的主要信息
        anime_name = data['animeName']+" "  # 获取漫画的名称
        anime_title = data['title']+" "     # 获取漫画的话标题
        anime_num = str(data['numberStart'])+" "  # 获取漫画的话号
        url_list = data['contentImg']  # 获取这一话所有图片的url组成的列表
        for j in url_list:  # 对这一话所有图片的url组成的列表遍历，写入对应文件
            text = anime_name+anime_title+anime_num+j['url']+" "+j['name']+'\n'
            with open(download_filename, 'ab') as f:
                f.write(text.encode())
        cnt = cnt+1
        print("No."+str(cnt)+" "+anime_num+anime_title+'has downloaded') # 每下载好一话输出确认信息
    return download_filename  # 返回保存URL的文件的地址


if __name__ == '__main__':
    #存储每一话所有图片的URL 填充不同id值即可找到所有图片URL
    base_url = 'https://prod-api.ishuhui.com/comics/detail?id={}'
    download_filename = 'W:\\漫画\\URL\\一拳超人URL.txt'
    num_filename = 'W:\\漫画\\尾缀\\一拳超人.txt'
    get_all_img_url(base_url, download_filename, num_filename)