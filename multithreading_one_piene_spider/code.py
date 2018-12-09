# coding:utf-8
from selenium import webdriver
import re
import time
import timeit
import threading
import queue


def get_img_url(base_url, save_file, idx, driver):
    url = base_url.format(idx)
    driver.get(url)
    content = driver.find_elements_by_class_name('comic-contain')  # 定位到主体漫画部分
    if not content:  # 如果没有定位到说明此URL没有所需内容直接跳过
        pass
    else:  # 如果链接存在继续运行
        print('downloading')
        ans = content[0].find_elements_by_class_name('comic-text')  # 定位这一话中每一张图片
        for i in ans:
            try:
                i.click()    # 点击 滚动条滚动到相应图片并加载
            except:
                time.sleep(0.3)  # 等待图片加载完成
        time.sleep(0.3)  # 最后等待一会 等待图片加载完成
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


class my_thread(threading.Thread):
    # def __init__(self):
    #     super().__init__() # 继承
    #     如果想给线程添加属性可加在此处

    def run(self):
        print(self.name, 'is running')
        # driver = webdriver.Chrome() # 使用此行 注释下面3行为有界面模式
        chrome_options = webdriver.ChromeOptions()  # 无界面模式
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)  # 打开浏览器
        while not q.empty():
            print(self.name, 'is downloading')
            idx = q.get()
            get_img_url(base_url, save_file, idx,driver)
        driver.close()


if __name__ == '__main__':
    threads = []
    q = queue.Queue()  # 创建队列
    for i in range(1, 100):  # 下载1到100话可自行设定
        q.put(i)
    pattern = '(manhua.qpic.cn/manhua_detail/0.*?.jpg/0)'
    tpattern = '<title>《航海王》(.*?)-'
    base_url = 'http://ac.qq.com/ComicView/index/id/505430/cid/{}'
    save_file = 'W:\\漫画\\URL\\测试\\temp.txt'  # 所有图片URL的保存地址，可自行修改
    time1 = timeit.default_timer()
    for i in range(2):   # 开启的线程数 可自行修改
        t = my_thread()  # 创建线程
        t.start()        # 开启线程并调用线程的run方法
        threads.append(t)  # 将线程加入队列threads
    for t in threads:
        t.join()   # 等待各个线程结束
    time2 = timeit.default_timer()
    print('the download took %d s' % (time2-time1))
