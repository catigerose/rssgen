from feed_funcs import gen_fg, feeds_url, feeds_dir, get_entrys, tz
import requests
from datetime import datetime
from datetime import date, timedelta
import requests
import time
from bs4 import BeautifulSoup

def get_soup(url):
        headers = {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", }
        ret = requests.get(url, headers=headers, timeout=5)        
        ret.encoding = "utf-8"
        time.sleep(1)
        soup = BeautifulSoup(ret.text, features="lxml")  # 构建beautifulsoup实例
        return soup

if __name__ == '__main__':

    feed_title = "人民日报"  # feed的标题，会显示在feed阅读器中
    feed_description = "人民日报每日重要新闻"  # feed的描述
    feed_name = "renmrb.xml"  # feed xml文件的的名字
    website_url = "http://paper.people.com.cn/"  # 要爬取的页面

    feed_path = feeds_dir + feed_name
    feed_url = feeds_url + feed_name
    titles, contents, links, guids, updateds, publisheds = get_entrys(
        feed_path)
    new_nums = 0
    old_nums = len(guids)

    
    # 先尝试获取今天的新闻，若404，则改为昨天。
    today = date.today() 
    yesterday = date.today() - timedelta(days=1)

    today_url = f"http://paper.people.com.cn/rmrb/pc/layout/{today.year}{str(today.month).zfill(2)}/{str(today.day).zfill(2)}/node_01.html"
    headers = {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", }
    ret = requests.get(today_url, headers=headers, timeout=5)
    if ret.status_code==404:
        latest_day = yesterday
    else:
        latest_day = today

    # 以下生成、汇总子版面的url，周末排版不一样
    year =latest_day.year
    month = str(today.month).zfill(2)
    day = str(today.day).zfill(2)
    weekday =latest_day.weekday()  # 周末排版不一样
    str_today = '{}{}/{}/'.format(year, month, day)  # 拼接成url需要的格式
    domain = "http://paper.people.com.cn/rmrb/pc/layout/"+str_today  # url和新闻详情页 前面公用的域名
    spaces1 = ["01.html", "02.html", "03.html", "04.html", "05.html", "06.html",
                "07.html", "08.html", "09.html", "10.html", "14.html", "17.html"]  # 工作日新闻版面类别
    spaces2 = ["01.html", "02.html", "03.html", "04.html", "05.html"]  # 周末新闻版面类别
    if weekday in [5, 6]:
        spaces = spaces2
    else:
        spaces = spaces1
    urls = []
    for space in spaces:
        urls.append(domain+"node_" + space)

    # 3. 获取新闻内容
    for url0 in urls:

        soup = get_soup(url0)  # 网页的内容，返回bs4的soup文件
        if soup.find("ul", class_="news-list"):

            news_list = soup.find(
                "ul", class_="news-list").find_all("a")  # 获取新闻列表
            # news_list.reverse()
            for news in news_list:

                news_title = news.get_text()  # 新闻的标题
                
                

                # 过滤一些报道
                filter_strings = ["责编", "图片报道", "广告"]
                filter_results = []
                for str in filter_strings:
                    filter_result = news_title.find(str) == -1
                    filter_results.append(filter_result)
                if False in filter_results:
                    pass

                else:
                    news_url = domain + news.attrs['href']  # 详情页的url
                    guid = news_url

                    if guid not in guids:
                        news_detail = get_soup(news_url).find(
                            "div", class_="article").decode()  # 获取新闻内容详情

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
