from feed_funcs import get_soup, gen_fg, feeds_url, feeds_dir, get_entrys, tz
from datetime import datetime

if __name__ == '__main__':

    feed_title = "华尔街见闻-最新资讯"  # feed的标题，会显示在feed阅读器中
    feed_description = "华尔街见闻实时新闻，7*24金融资讯，不仅更快还要你懂，华尔街，财经数据，24小时资讯，最新，股市，债市，商品，外汇，公司，资管，科技，硬AI，地产，汽车，医药"  # feed的描述
    feed_name = "wallstreet_news.xml"  # feed xml文件的的名字
    website_url = 'https://wallstreetcn.com/news/global'  # 要爬取的页面

    feed_path = feeds_dir + feed_name
    feed_url = feeds_url + feed_name
    titles, contents, links, guids, updateds, publisheds = get_entrys(
        feed_path)
    new_nums = 0
    old_nums = len(guids)

    news_list = get_soup(website_url, 1).find("div",class_="article-list").find_all("div",class_="article-entry list-item")
    

    # print(news_list)
    news_list.reverse()  # 新的news排在列表后面
    for news in news_list:
        news_url = news.div.a.attrs['href']
        guid = news_url

        if guid not in guids:

            news_title = news.div.a.get_text()  # 新闻的标题
            news_detail = get_soup(news_url,1).find(
                "div", class_="rich-text").decode()


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
