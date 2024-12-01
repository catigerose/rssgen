from feed_funcs import get_soup, gen_fg, feeds_url, feeds_dir, get_entrys, tz
from datetime import datetime
from datetime import date

if __name__ == '__main__':

    feed_title = "证券日报"  # feed的标题，会显示在feed阅读器中
    feed_description = "证券日报每日重要新闻"  # feed的描述
    feed_name = "zqrb.xml"  # feed xml文件的的名字
    website_url = "http://epaper.zqrb.cn/"  # 网站主页
    feed_path = feeds_dir + feed_name
    feed_url = feeds_url + feed_name
    titles, contents, links, guids, updateds, publisheds = get_entrys(
        feed_path)
    new_nums = 0
    old_nums = len(guids)

    # 1. 获取今天的日期（年，月，日）
    today = date.today()
    year = today.year
    month = str(today.month).zfill(2)
    day = str(today.day).zfill(2)
    weekday = today.weekday()  # 周末排版不一样
    str_today = '{}-{}/{}/'.format(year, month, day)  # 拼接成url需要的格式
    # str_today
    # 2. 获取每个版面的链接
    domain = "http://epaper.zqrb.cn/html/" + \
        str_today + "node_2.htm"  # url和新闻详情页 前面公用的域名

    soup = get_soup(domain)

    tables = soup.find("div", class_="neir").find_all(
        "table", class_="biaoge")[:9]
    urls = []

    for table in tables:
        if table.find("h2").get_text().strip()[2:] not in ["信息披露", "艺术投资"]:
            links2 = table.find_all("table")[-1].find_all("a")
            for link in links2:
                urls.append("http://epaper.zqrb.cn/html/" +
                            str_today+link.attrs['href'])

    for news_url in urls:

        guid = news_url
        # print(news_url)

        if guid not in guids:

            news_detail = get_soup(news_url).find(
                "div", class_="neiyee").decode()  # # 获取新闻内容详情
            news_title = get_soup(news_url).find(
                "div", class_="neiyee").find("h1").get_text().strip()  # 新闻的标题

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
