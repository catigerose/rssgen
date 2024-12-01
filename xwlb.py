#!/usr/bin/env python
# coding: utf-8
from feed_funcs import get_soup, gen_fg, feeds_url, feeds_dir, get_entrys, tz
from datetime import datetime


def get_content(news_url):
    detail_soup = get_soup(news_url)  # 构建beautifulsoup实例
    if detail_soup.find("div", id="content_area"):
        news_detail = detail_soup.find("div", id="content_area").decode()
    else:
        news_detail = detail_soup.body.decode()
    # news_detail = detail_soup.find("div", class_="g-article").decode()
    import time
    time.sleep(0.5)  # 间隔时间防止反爬虫
    return news_detail


if __name__ == '__main__':

    # 该部分变量每个feed均不同，且必须填写。
    feed_name = "xwlb.xml"  # feed xml文件的的名字
    website_url = 'http://tv.cctv.com/lm/xwlb/'  # 要爬取的页面，也是feed的link
    feed_title = "新闻联播"  # rss的标题，会显示再rss阅读中
    feed_description = "《新闻联播》是中国中央电视台每日晚间播出的一档新闻节目，被称为“中国政坛的风向标”，节目宗旨为“宣传党和政府的声音，传播天下大事”。"  # rss的描述

    feed_path = feeds_dir + feed_name
    feed_url = feeds_url + feed_name
    titles, contents, links, guids, updateds, publisheds = get_entrys(
        feed_path)
    new_nums = 0
    old_nums = len(guids)

    # 该部分为爬虫模块，不同feed一般不一样
    soup = get_soup(website_url, 1)  # 网页的内容，返回bs4的soup文件
    news_list = soup.find("ul", id="content").find_all("li")

    news_list.reverse()  # 新的news排在列表后面
    for news in news_list[1:]:
        news_url = news.a.attrs['href']  # 详情页的url
        guid = news_url

        if guid not in guids:
            news_title = news.a.attrs['title']  # 新闻的标题
            news_detail = get_content(news_url)

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
