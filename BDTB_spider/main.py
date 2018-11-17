# coding:utf-8
import urllib.request
import re
import os
import timeit


class simple_crawler:
    def __init__(self, url, pattern):
        self.url = url
        self.pattern = pattern

    def get_page(self):
        request = urllib.request.Request(self.url)
        response = urllib.request.urlopen(request)
        print('get the source of web', self.url)
        return response

    def get_imgs_url(self):
        res = self.get_page().read().decode("utf-8")
        all_blank = ['\n', '\r']  # 此处去除换行符  未测试
        for i in all_blank:
            res = res.replace(i, '')
        imgs = re.findall(self.pattern, res)
        print("get the img's url")
        return imgs

    def download_imgs(self, filename):
        try:
            os.makedirs(filename)  # 创建文件
            print('create file', filename)
        except OSError:
            print('OSError happened', filename, 'is exists')
        imgs = self.get_imgs_url()
        idx = 1
        for img in imgs:
            print('one piece', idx, 'is downloading')
            img = urllib.request.urlopen(img[2]).read()  # 此处的img[2]因为正则的第3个字符串是需要的网页
            img_file = filename + '\\' + str(idx) + '.jpg'
            idx = idx + 1
            with open(img_file, 'wb') as f:
                f.write(img)


url = "https://tieba.baidu.com/p/5934835791?see_lz=1"  # 目标网页URL
pattern = '(<img class="BDE_Image".*?)(src=")(.+?jpg)'
filename = r'W:\python3爬取百度贴吧图片\onepiece'  # 输入你想下载到的位置
ans = simple_crawler(url, pattern)
time1 = timeit.default_timer()
ans.download_imgs(filename)
time2 = timeit.default_timer()
print('the download took %d s' % (time2-time1))