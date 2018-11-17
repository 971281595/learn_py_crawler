# coding:utf-8
import urllib.request
from selenium import webdriver
import re
import json
import os
import timeit


def get_all_url(base_url, pattern, filename):#获取每一话的id
    """参数1漫画首页URL 参数2漫画每一话URL的正则 参数3存放的文件地址"""
    driver = webdriver.Chrome()  # 打开Chrome浏览器
    driver.get(base_url)    # 打开对应漫画首页URL
    ans = []         # ans存放url的尾缀
    all_content = driver.find_elements_by_css_selector('.ant-tabs-nav.ant-tabs-nav-animated')
    content = all_content[1].find_elements_by_class_name('ant-tabs-tab')
    for i in range(0, len(content)):
        if content[i].text == "": # 若按钮不存在则退出
            break
        content[i].click()   # 点击相应按钮
        page = driver.page_source  # 获取包含每一话url的源代码
        print('page=', page)
        partial_url = re.findall(pattern, page)#匹配源代码中的url
        ans.append(partial_url) # 添加url到ans列表
    driver.close() # 关闭Chrome浏览器
    all_url = set()
    for i in ans:  # 将ans去重保存在all_url集合
        for j in i:
            all_url.add(j[1])
    with open(filename, 'wb+') as f: #写入到filename中
        for i in all_url:
            print(i, ' is downloading')
            f.write(i.encode())
            f.write('\n'.encode())
    return filename     # 返回存储尾缀的文件地址


if __name__ == '__main__':
    url = 'https://www.ishuhui.com/comics/anime/53'
    pattern = r'(comics.detail.(.*?))"'
    filename = 'W:\\漫画\\尾缀\\一拳超人.txt'
    get_all_url(url, pattern, filename)