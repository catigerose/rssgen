
from feed_funcs import get_soup, gen_fg, feeds_url, feeds_dir, get_entrys, tz
from datetime import datetime
# 该函数获取详情页的新闻内容


def get_content(news_url):

    detail_soup = get_soup(news_url, 1)   # 构建beautifulsoup实例
    if detail_soup.find("div", id="content"):  # 获取新闻内容详情
        news_detail = detail_soup.find("div", id="content").decode()
    else:
        news_detail = detail_soup.body.decode()  # 直接将详情页body做为新闻详情

    if detail_soup.find("p", class_="ftEditor"):  # 获取新闻内容详情
        source = detail_soup.find("p", class_="ftEditor").get_text()
    else:
        source = "未显示来源"  # 直接将详情页body做为新闻详情
    import time
    time.sleep(0.5)  # 间隔时间防止反爬虫
    return news_detail, source


if __name__ == '__main__':

    website_url = 'https://news.futunn.com/main?lang=zh-cn'  # 要爬取的页面
    feed_title = "富途牛牛要闻"  # feed的标题，会显示在feed阅读器中
    feed_name = "futunn.xml"  # feed xml文件的的名字
    feed_description = "财经新闻_最新全球财经资讯报道 - 富途牛牛"  # feed的描述

    feed_path = feeds_dir + feed_name
    feed_url = feeds_url + feed_name
    titles, contents, links, guids, updateds, publisheds = get_entrys(
        feed_path)
    new_nums = 0
    old_nums = len(guids)

    soup = get_soup(website_url, 1)  # 网页的内容，返回bs4的soup文件

    # 找到或精确 items位置  ，防止抓到其它版面内容
    news_list = soup.find(
        "div", class_="market-wrap").find_all("a", class_="market-item list-item")

    news_list.reverse()  # 新的news排在列表后面
    for news in news_list:
        news_url = news.attrs['href']  # 详情页的url
        guid = news_url

        if guid not in guids:
            news_title = news.h2.get_text()  # 新闻的标题
            news_detail, source = get_content(news_url)

            # 过滤一些报道
            filter_strings = ["智通财经", "华尔街见闻", "格隆汇"]
            filter_results = []
            for keyword in filter_strings:
                filter_result = source.find(keyword) == -1
                filter_results.append(filter_result)

            if False in filter_results:
                pass
            else:

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
