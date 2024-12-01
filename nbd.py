from feed_funcs import get_soup, gen_fg, feeds_url, feeds_dir, get_entrys, tz
from datetime import datetime


# 该函数获取详情页的新闻内容
def get_content(news_url):
    detail_soup = get_soup(news_url)  # 构建beautifulsoup实例
    if detail_soup.find("div", class_="g-articl-text"):
        news_detail = detail_soup.find("div", class_="g-articl-text").decode()
    else:
        news_detail = detail_soup.body.decode()

    # news_detail = detail_soup.find("div", class_="g-article").decode()
    import time
    time.sleep(0.5)  # 间隔时间防止反爬虫
    return news_detail


# # 4.生成RSS的xml文件
if __name__ == '__main__':

    feed_title = "要闻-每日经济新闻"  # feed的标题，会显示在feed阅读器中
    feed_description = "每经网是24小时新闻网站，依托新锐财经日报《每日经济新闻》打造中国具有影响力的新闻网站，覆盖品牌价值、汽车资讯、视频、基金、财经、房产、金融新闻、券商、公司等方向，是全方位财经新闻平台。"  # rss的描述
    feed_name = "nbd.xml"  # feed xml文件的的名字
    website_url = 'http://www.nbd.com.cn/columns/3/'  # 要爬取的页面

    feed_path = feeds_dir + feed_name
    feed_url = feeds_url + feed_name
    titles, contents, links, guids, updateds, publisheds = get_entrys(
        feed_path)
    new_nums = 0
    old_nums = len(guids)

    soup = get_soup(website_url)  # 网页的内容，返回bs4的soup文件
    news_list = soup.find(
        "ul", class_="u-news-list").find_all("li", class_="u-news-title")

    news_list.reverse()  # 新的news排在列表后面
    for news in news_list:
        news_url = news.a.attrs['href']  # 详情页的url
        guid = news_url

        if guid not in guids:
            news_title = news.a.get_text()  # 新闻的标题
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
