#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from selenium import webdriver
from urllib.parse import quote
import re
import pandas
import time
import random


def get_url(url, key):  # 查找一个页面内所有的商品的链接，目前只找一个页面的商品的链接
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    driver.implicitly_wait(3)
    # 利用xpanth找出当前页面所有商品的链接
    # 1.在URL的页面选中某一元素，在F12的开发工具内，点击对应元素的右键
    # 2.copy—>xpath.
    # 3.即可取到某元素的xpath
    table = driver.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li/div/div[1]/a')
    urls = []
    for i in table:
        link = i.get_attribute('href')
        if re.match(r'https://item.jd.com/[0-9]+.html', link):
            urls.append(link)
    # for u in urls:
    #     print(u)
    driver.close()
    driver.quit()
    return urls


def get_comment(url_comment):  # 获取每一页评论，但不是获取具体的评论内容
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    brower = webdriver.Firefox(options=options)  #启用无头模式 options=options
    brower.get(url_comment + '#comment')  # 拼接评论页面
    brower.implicitly_wait(20)  # 进行隐式等待
    comment = []  # 保存评论
    flag = 0
    # get_page_comment(brower, comment)
    while True:
        # print(comment)
        flag = flag + 1
        if flag > 100:
            break
        # 找到具体的评论
        print('第' + str(flag) + '页')
        # 下面是针对评论不够100页，但是不够的依然有下一页按钮，就找无评论的div，提早结束程序
        zhang = brower.find_elements_by_class_name('ac comments-item')
        # if zhang == []:
        #     print(brower.find_elements_by_class_name('ac comments-item'))
        #     pass
        # else:
        #     print('爬取完毕！评论只有' + str(flag) + '页！')
        #     break
        # flag = int(flag)
        try:
            brower.find_element_by_class_name('ui-pager-next').click()
            brower.implicitly_wait(5)
            # brower.execute_script("window.scrollBy(0,4000)")  # 执行javascript语句
            flag_end = get_page_comment(brower, comment)
            print('爬取状态：' + flag_end)
            if flag_end == 'End':
                print('爬取完毕！评论只有' + str(flag) + '页！')
                break
        except:
            # get_page_comment(brower, comment)
            print('爬取完毕！')
            break
        time.sleep(15 + random.randint(20, 100) / 20)
        # get_page_comment(brower, comment)
    save_to_csv(comment)
    brower.close()
    brower.quit()


def get_page_comment(brower, comment):  # 获取到页面内的具体评论
    try:
        data = brower.find_elements_by_class_name('comment-con')
        if data == []:  # 获取到的评论数据为空，代表已经没有评论了
            return 'End'
        for i in data:
            text = i.text
            if re.match(r'此用户未填写评价内容', text):
                continue
            else:
                if text not in comment:
                    comment.append(text)
                    print(text)
    except:  # 不知道为什么会出现数据已经读取的现象
        print('该页面已获取！')
        pass
        # print('页面已刷新，从新获取comment！')
        # data = brower.find_elements_by_class_name('comment-con')
        # for i in data:
        #     text = i.text
        #     if re.match(r'此用户未填写评价内容', text):
        #         continue
        #     else:
        #         comment.append(text)
                # print(i.text)
    return 'Yes'


def save_to_csv(comment):
    i = 1
    with open('jingdong_comment.txt', 'a', encoding='utf-8') as f:
        for u in comment:
            f.writelines('第' + str(i) + '条：' + u + '\n')
            i = int(i)
            i = i + 1
    comment = pandas.DataFrame(comment)
    comment.to_csv('jingdong_comment.csv')


if __name__ == '__main__':
    key = 'iphone x'
    url = 'https://search.jd.com/Search?keyword=' + quote(key) + '&enc=utf-8'  # 拼接查找的页面
    urls = get_url(url, key)
    # for i in urls:
    #     print(i)
    get_comment(urls[0])
    get_comment('https://item.jd.com/11794447957.html')

