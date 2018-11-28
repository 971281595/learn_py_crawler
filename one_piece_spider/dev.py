# coding:utf-8
from selenium import webdriver
import re
import time
import timeit


def get_img_url(base_url, save_file):
    driver = webdriver.Chrome()  # 将此行注释 换成执行下面三行启用无界面模式
    # chrome_options = webdriver.ChromeOptions()  # 无界面模式
    # chrome_options.add_argument('--headless')
    # driver = webdriver.Chrome(options=chrome_options)  # 打开浏览器
    for idx in range(1, 693):   # 获取从第一话到最后一话的URL
        url = base_url.format(idx)
        driver.get(url)
        content = driver.find_elements_by_class_name('comic-contain')  # 定位到主体漫画部分
        if not content:  # 如果没有定位到说明此URL没有所需内容直接跳过
            continue
        else:
            print('downloading')
        ans = content[0].find_elements_by_class_name('comic-text')  # 定位这一话中每一张图片
        for i in ans:
            try:
                time.sleep(0.3)  # 等待图片加载完成
                i.click()    # 点击 滚动条滚动到相应图片并加载
            except:
                pass
        page = driver.page_source
        imgs = re.findall(pattern, page)
        tmptitle = re.search(tpattern, page)
        title = tmptitle[1].replace(' ', '')   # 获取话标题
        with open(save_file, 'ab') as f: # 将URL及话标题存入相应文件
            cnt = 1
            f.write((title+'\n').encode())
            for img_url in imgs:
                res = img_url + "," + str(cnt) + '\n'
                f.write(res.encode())
                cnt = cnt + 1
        print(title, 'has downloaded')
    driver.close()  # 关闭浏览器


pattern = '(manhua.qpic.cn/manhua_detail/0.*?.jpg/0)'
tpattern = '<title>《航海王》(.*?)-'
base_url = 'http://ac.qq.com/ComicView/index/id/505430/cid/{}'
save_file = 'W:\\漫画\\URL\\testt.txt' # 所有图片URL的保存地址，可自行修改
time1 = timeit.default_timer()
get_img_url(base_url, save_file)
time2 = timeit.default_timer()
print('the download took %d s' % (time2-time1))