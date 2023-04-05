from feed_funcs import get_soup, gen_fg, feeds_url, feeds_dir, get_entrys, tz
from datetime import datetime

if __name__ == '__main__':

    
    feed_title = "期货新闻-英为财情"  # feed的标题，会显示在feed阅读器中
    feed_description = "期货新闻_全球最新商品、股指、外汇期货资讯一览_英为财情Investing.com"  # feed的描述
    feed_name =  "commodities_news.xml"  # feed xml文件的的名字
    website_url = 'https://cn.investing.com/news/commodities-news'  # 要爬取的页面
    
    feed_path = feeds_dir + feed_name
    feed_url = feeds_url + feed_name
    titles, contents, links, guids, updateds, publisheds = get_entrys(  feed_path)
    new_nums = 0
    old_nums = len(guids) 
    
    
    soup = get_soup(website_url,1).find(
        "section", id="leftColumn")  # 网页的内容，返回bs4的soup文件
    news_list = soup.find_all(
        "article", class_="js-article-item articleItem")  # 找到或精确 items位置

    news_list.reverse()  # 新的news排在列表后面  
    for news in news_list:
        news_url = "https://cn.investing.com"+news.a.attrs['href']  # 详情页的url
        guid = news_url


        if guid not in guids:             
            news_title = news.div.a.get_text()  # 新闻的标题
            # print(news_title)
            #news_detail = get_soup(news_url,True, chromedriver_path).find("div", class_="WYSIWYG articlePage").decode()
            news_detail = news.div.get_text()

            
                      
            new_nums += 1
            titles.append(news_title)
            contents.append(news_detail)
            links.append(news_url)
            guids.append(guid)
            updateds.append(datetime.now(tz))
            publisheds.append(datetime.now(tz))
    truc = min(old_nums,new_nums) # 保证不漏掉新的内容，没有feed文件则新的全部写入，及限制entry数目
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
