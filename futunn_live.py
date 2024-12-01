

from feed_funcs import get_soup, gen_fg, feeds_url, feeds_dir, get_entrys, tz, get_json
import json
from datetime import datetime

if __name__ == '__main__':

    feed_name = "futunn_live.xml"  # feed xml文件的的名字
    website_url = 'https://news.futunn.com/main/live?lang=zh-cn/'  # 要爬取的页面
    feed_title = "富途牛牛-快讯"  # feed的标题，会显示在feed阅读器中
    feed_description = "7×24小时全球实时财经新闻快讯 - 富途牛牛"  # feed的描述

    feed_path = feeds_dir + feed_name
    feed_url = feeds_url + feed_name
    titles, contents, links, guids, updateds, publisheds = get_entrys(
        feed_path)
    new_nums = 0
    old_nums = len(guids)

    url = "https://news.futunn.com/news-site-api/main/get-flash-list?pageSize=30"

    soup = get_soup(url, 1)

    pre = soup.body.pre.get_text()

    res = json.loads(pre)

    news_list = res['data']['data']["news"]

    news_list.reverse()  # 新的news排在列表后面
    for news in news_list:

        news_url = "https://news.futunn.com/flash/" + str(news["id"])
        guid = news_url
        news_detail = news["content"]
        pub_time = datetime.fromtimestamp(int(news["time"]), tz)

        news_title = news["title"]
        if news_title == "":
            news_title = news_detail

        if guid not in guids:
            new_nums += 1
            titles.append(news_title)
            contents.append(news_detail)
            links.append(news_url)
            guids.append(guid)
            updateds.append(pub_time)
            publisheds.append(pub_time)
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
