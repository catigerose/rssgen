from feed_funcs import get_soup, gen_fg, feeds_url, feeds_dir, get_entrys, tz
from datetime import datetime

if __name__ == '__main__':

    feed_name = "cls_telegraph.xml"  # feed xml文件的的名字
    website_url = 'https://www.cls.cn/telegraph/'  # 要爬取的页面
    feed_title = "财联社电报"  # feed的标题，会显示在feed阅读器中
    feed_description = "财联社电报中心，A股24小时电报。为投资者提供专业的上市公司动态、股市资讯、股票行情、财经新闻、今日股市行情、创业板、新能源汽车、板块投资资讯。"  # feed的描述

    feed_path = feeds_dir + feed_name
    feed_url = feeds_url + feed_name
    titles, contents, links, guids, updateds, publisheds = get_entrys(
        feed_path)
    new_nums = 0
    old_nums = len(guids)

    soup = get_soup(website_url, 1)  # 网页的内容，返回bs4的soup文件
    # 找到或精确 items位置  ，防止抓到其它版面内容
    news_list = soup.find_all("div", class_="clearfix p-r l-h-26p")

    # entry必须使用url作为唯一性的id，相同id entry rss阅读不会再抓取。
    # 直播类网站可能没有url，使用detail生成hash制作伪url。
    from hashlib import md5

    news_list.reverse()  # 新的news排在列表后面

    for news in news_list:
        news = news.find_all("span")[1].div
        news_detail = news.get_text()
        guid = website_url + \
            md5(news_detail.encode(encoding='utf-8')).hexdigest()

        if guid not in guids:

            if news.strong:
                news_title = news.strong.get_text()
            else:
                news_title = news_detail  # 新闻的标题

            news_url = guid  # 详情页的url

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
