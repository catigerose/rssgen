
from feed_funcs import get_soup, gen_fg, feeds_url, feeds_dir, get_entrys, tz
from datetime import datetime

if __name__ == '__main__':

    id_list = [231729, 273399, 241263, 241737,
               225389, 268767, 263711, 238420, 215408]

    feed_titles = [x+"-同花顺投顾" for x in ["光大期货", "中信建投期货",
                                        "平安期货", "长城证券期货", "徽商期货", "广州期货", "华创期货", "钱多多团队", "南华期货"]]
    feed_descriptions = [x+"-同花顺投顾平台，http://t.10jqka.com.cn/newcircle/" for x in [
        "光大期货", "中信建投期货", "平安期货", "长城证券期货", "徽商期货", "广州期货", "华创期货", "钱多多团队", "南华期货"]]
    feed_names = [str(x)+".xml" for x in id_list]

    for i in range(len(id_list)):
        feed_name = feed_names[i]
        feed_description = feed_descriptions[i]
        feed_title = feed_titles[i]

        feed_path = feeds_dir + feed_name
        feed_url = feeds_url + feed_name
        # 要爬取的页面
        website_url = 'http://t.10jqka.com.cn/circle/{}/'.format(id_list[i])

        titles, contents, links, guids, updateds, publisheds = get_entrys(
            feed_path)
        new_nums = 0
        old_nums = len(guids)

        soup = get_soup(website_url, 1)
        news_list = soup.find(
            "ul", class_="postlist-ul").find_all("li", class_="post-single clearfix")
        news_list.reverse()
        for li in news_list:
            news_url = li.find("a").attrs['href']
            guid = news_url
            if guid not in guids:
                news_title = li.find("a").find(
                    "div", class_="post-title").get_text()  # 新闻的标题
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
