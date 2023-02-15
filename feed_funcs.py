
from datetime import datetime
import requests
import time
from bs4 import BeautifulSoup
from platform import system
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from feedgen.feed import FeedGenerator
from pytz import timezone
import feedparser
import json

# 根据操作系统指定工作目录，使代码在linux和windows都能运行。
if system() == 'Linux':
    work_dir = "/usr/share/rssgen"
    chromedriver_path = "/usr/share/rssgen/chromedriver-linux/chromedriver" # chromedriver的路径
elif system() == 'Windows':
    work_dir = "."
    chromedriver_path = "./chromedriver-windows/chromedriver"  # chromedriver的路径
    
else:
    print("waring： platform.system is not linux or windows")
    work_dir = "."



feeds_dir = work_dir + "/feeds/"   # feed 的存放目录
feeds_url = "http://rss.catigerose.fun/feeds/"  # feed是 存放目录的url

# 获取 任何网页的内容，返回bs4的soup文件
tz = timezone('Asia/Shanghai')

def get_soup(url, is_dynamic=False):

    if is_dynamic:
        options = Options()  # 实例化一个chrome浏览器实例对象
        options.add_argument("headless")  # 不打开浏览器窗口 运行selenium
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-gpu")
        # options.add_argument("--remote-debugging-port=9222")  # this

        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
        options.add_argument('--user-agent=%s' % user_agent)

        # 函数更新，使用service传参数，解决警告 DeprecationWarning: executable_path has been deprecated, please pass in a Service object
        s = Service(chromedriver_path)
        driver = Chrome(service=s, options=options)  # 新建driver
        driver.maximize_window()  # 最大化窗口

        driver.get(url)  # 获取页面内容
        time.sleep(2)  # 等待5s，等待加载完成

        page_source = driver.page_source  # 获取页面源码数据
        soup = BeautifulSoup(page_source, features="lxml")  # 用 BeautifulSoup解析
        driver.close()

    else:
        # 请求头
        headers = {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", }
        ret = requests.get(url, headers=headers)
        ret.encoding = ret.apparent_encoding
        time.sleep(1)
        soup = BeautifulSoup(ret.text, 'html.parser')  # 构建beautifulsoup实例
    return soup


def gen_fg(website_url, feed_title, feed_description, feed_url, entry_titles, entry_details,entry_urls, guids,updateds,publisheds,truc=0):

    
    fg = FeedGenerator()
    # 使用网站标题作为feed标题   Contains a human readable title for the feed
    fg.title(feed_title)
    # Indicates the last time the feed was modified in a significant way.
    fg.updated(datetime.now(tz))
    # 使用爬取网站url作为具有唯一性的id   Identifies the feed using a universally unique and permanent URI.
    fg.id(website_url)
    # feed指向的网页  Identifies a related Web page
    fg.link(href=website_url, rel='alternate')
    # A feed should contain a link back to the feed itself
    fg.link(rel='self', type="application/atom+xml", href=feed_url)

    # feed的作者 Names one author of the feed.
    fg.author(name='catigerose', email='catigerose@gmail.com')
    fg.subtitle(feed_description)  # 使用网站描述作为feed描述
    #fg.language(lang)
    # fg.logo('http://ex.com/logo.jpg')
    #fg.contributor( name='catigerose', email='catigerose@gmail.com' )
    # fg.icon('http://ex.com/logo.jpg') #Icons should be square

    for i  in range(truc,len(guids)):
        fe = fg.add_entry()

        fe.title(entry_titles[i])
        fe.content(entry_details[i],type="html")
        fe.link(href=entry_urls[i])
        fe.id(id=guids[i])
        fe.updated(updateds[i])
        fe.published(publisheds[i])

    return fg


# 解析 itom种子
def get_entrys(feed_path):
    
    d = feedparser.parse(feed_path)   
    
    titles = []
    contents = []
    links = []
    guids = []
    updateds = []
    publisheds = []
    d.entries.reverse() # 使较新的entry 在列表后面
    for entry in d.entries:  
        
        titles.append(entry.title)
        contents.append(entry.content[0].value)
        links.append(entry.link)
        guids.append(entry.guid)
        updateds.append(entry.updated)
        publisheds.append(entry.published)
    
    return titles,contents,links,guids,updateds,publisheds

# 获取api接口数据，并用python json解析，返回字典
def get_json(url):
    headers = {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", }

    ret = requests.get(url, headers=headers).text
    data = json.loads(ret)
    return data