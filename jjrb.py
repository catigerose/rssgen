from feed_funcs import get_soup, gen_fg, feeds_url, feeds_dir, get_entrys, tz
from datetime import datetime
from datetime import date, timedelta

if __name__ == '__main__':

    feed_title = "经济日报"  # feed的标题，会显示在feed阅读器中
    feed_description = "经济日报每日重要新闻"  # feed的描述
    feed_name = "jjrb.xml"  # feed xml文件的的名字
    website_url = "http://paper.ce.cn/pc/layout/"  # 要爬取的页面

    feed_path = feeds_dir + feed_name
    feed_url = feeds_url + feed_name
    titles, contents, links, guids, updateds, publisheds = get_entrys(
        feed_path)
    new_nums = 0
    old_nums = len(guids)

    # 1. 获取今天的日期（年，月，日）,网页改版，改成获取昨天的日期
    today = date.today() - timedelta(days=1)
    year = today.year
    month = str(today.month).zfill(2)
    day = str(today.day).zfill(2)
    weekday = today.weekday()  # 周末排版不一样
    str_today = '{}{}/{}/'.format(year, month, day)  # 拼接成url需要的格式
    # str_today
    # 2. 获取每个版面的链接
    domain = "http://paper.ce.cn/pc/layout/" + str_today  # url和新闻详情页 前面公用的域名
    spaces = [
        "01.html", "02.html", "03.html", "04.html", "05.html", "06.html",
        "07.html", "08.html", "09.html", "10.html", "11.html", "12.html"
    ]  # 工作日新闻版面类别

    urls = []
    for space in spaces:
        urls.append(domain + "node_" + space)
    # print(urls[0])
    # 3. 获取新闻内容
    for url0 in urls:

        soup = get_soup(url0)  # 网页的内容，返回bs4的soup文件
        if soup.find("ul", id="articlelist"):

            # 获取新闻列表
            news_list = soup.find("ul", id="articlelist").find_all("a")
            # news_list.reverse()
            for news in news_list:

                news_title = news.get_text()  # 新闻的标题

                # 过滤一些报道
                filter_strings = [
                    "责编", "图片报道", "广告", "图片新闻", "来稿邮箱", "公益", "邮箱"
                ]
                filter_results = []
                for str in filter_strings:
                    filter_result = news_title.find(str) == -1
                    filter_results.append(filter_result)
                if False in filter_results:
                    pass

                else:
                    news_url = "http://paper.ce.cn/pc" + news.attrs['href'][
                        8:]  # 详情页的url
                    guid = news_url
                    # print(news_url)

                    if guid not in guids:
                        news_detail = get_soup(news_url).find(
                            "div", class_="detail-art").decode()  # 获取新闻内容详情

                        new_nums += 1
                        titles.append(news_title)
                        contents.append(news_detail)
                        links.append(news_url)
                        guids.append(guid)
                        updateds.append(datetime.now(tz))
                        publisheds.append(datetime.now(tz))
    truc = min(old_nums, new_nums)  # 保证不漏掉新的内容，没有feed文件则新的全部写入，及限制entry数目
    # guids 唯一标记了entry，默认使用news_urls,news如无url，需要修改为news_titles
    fg = gen_fg(website_url, feed_title, feed_description, feed_url, titles,
                contents, links, guids, updateds, publisheds, truc)
    fg.atom_file(feed_path)  # Write the ATOM feed to a file
