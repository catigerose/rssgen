from feed_funcs import get_soup, gen_fg, feeds_url, feeds_dir, get_entrys, tz
from datetime import datetime


# # 4.生成RSS的xml文件
if __name__ == '__main__':

    feed_title = "中国宏观经济论坛（CMF）"  # feed的标题，会显示在feed阅读器中
    feed_description = "中国人民大学中国宏观经济论坛（CMF）成立于2006年，是中国宏观经济研究领域最有影响力的智库之一。"  # rss的描述
    feed_name = "cmf.xml"  # feed xml文件的的名字
    website_url = 'http://ier.ruc.edu.cn/index.htm'  # 要爬取的页面

    feed_path = feeds_dir + feed_name
    feed_url = feeds_url + feed_name
    titles, contents, links, guids, updateds, publisheds = get_entrys(
        feed_path)
    new_nums = 0
    old_nums = len(guids)

    soup = get_soup(website_url)  # 网页的内容，返回bs4的soup文件
    news_list = soup.find(
        "ul", class_="news_content").find_all("li")

    news_list.reverse()  # 新的news排在列表后面
    for news in news_list:
        news_url = news.a.attrs['href']  # 详情页的url
        guid = news_url

        if guid not in guids:
            news_title = news.find_all("a")[-1].get_text()  # 新闻的标题
            news_detail = news_title

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
