
from feed_funcs import gen_fg, feeds_url, feeds_dir, get_entrys, tz, get_json
from datetime import datetime

if __name__ == '__main__':

    # 该部分变量每个feed均不同，且必须填写。
    feed_name = "wallstreetcn_live.xml"  # feed xml文件的的名字
    website_url = 'https://wallstreetcn.com/live/global'  # 要爬取的页面，也是feed的link
    feed_title = "华尔街见闻-快讯"  # feed的标题，会显示在feed阅读器中
    feed_description = "华尔街见闻实时新闻，7*24金融资讯，不仅更快还要你懂，华尔街，财经数据，24小时资讯，7x24快讯，财经资讯，市场直播，黄金，黄金价格，原油，外汇，A股，美股，商品，股市"  # feed的描述

    feed_path = feeds_dir + feed_name
    feed_url = feeds_url + feed_name
    titles, contents, links, guids, updateds, publisheds = get_entrys(
        feed_path)
    new_nums = 0
    old_nums = len(guids)

    url = "https://api-one-wscn.awtmt.com/apiv1/content/lives?channel=global-channel&client=pc&limit=40&first_page=true&accept=live%2Cvip-live"
    data = get_json(url)
    news_list = data['data']['items']
    news_list.reverse()  # 新的news排在列表后面
    for news in news_list:
        news_url = news["uri"]  # 详情页的url
        guid = news_url

        news_detail = news["content_text"]

        news_title = news["title"]  # 新闻的标题
        if news_title == "":
            news_title = news_detail

        pub_time = datetime.fromtimestamp(news["display_time"], tz)

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
