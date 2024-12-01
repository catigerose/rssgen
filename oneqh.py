# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 11:26:57 2023

@author: catig
"""


from feed_funcs import gen_fg, feeds_url, feeds_dir, get_entrys, tz, get_soup

from datetime import datetime

if __name__ == '__main__':

    feed_name = "1qh_live.xml"  # feed xml文件的的名字
    website_url = 'https://www.1qh.cn/kx'  # 要爬取的页面
    feed_title = "一期货-快讯"  # feed的标题，会显示在feed阅读器中
    feed_description = "一期货快讯频道，不仅24小时不间断的为期货投资者提供期货市场最新最全快讯，还为期货投资者提供实时投资建议、最新研报、最新交易日历提醒、供需观察、产业检测等期货最新资讯。"  # feed的描述

    feed_path = feeds_dir + feed_name
    feed_url = feeds_url + feed_name
    titles, contents, links, guids, updateds, publisheds = get_entrys(
        feed_path)
    new_nums = 0
    old_nums = len(guids)

    soup = get_soup(website_url, 1)  # 网页的内容，返回bs4的soup文件
    # 找到或精确 items位置  ，防止抓到其它版面内容
    news_list = soup.find("ul", id="kx-content").find_all("li")

    news_list.reverse()  # 新的news排在列表后面

    for news in news_list:
        guid = news.attrs['id']
        if guid not in guids:
            news_url = "https://www.1qh.cn"+news.find("a").attrs['href']
            news_detail = news.find("a").get_text()
            news_title = news_detail  # 新闻的标题

            new_nums += 1
            titles.append(news_title)
            contents.append(news_detail)
            links.append(news_url)
            guids.append(guid)
            updateds.append(datetime.now(tz))
            publisheds.append(datetime.now(tz))
    truc = min(old_nums, new_nums)  # 保证不漏掉新的内容，没有feed文件则新的全部写入，及限制entry数目

    # guids 唯一标记了entry，默认使用news_urls,news如无url，需要修改为news_titles
    fg = gen_fg(website_url, feed_title, feed_description, feed_url,
                titles,
                contents,
                links,
                guids,
                updateds,
                publisheds,
                truc)
    fg.atom_file(feed_path)  # Write the ATOM feed to a file
