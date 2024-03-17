from feed_funcs import get_soup, gen_fg, feeds_url, feeds_dir, get_entrys, tz
from datetime import datetime

def get_content(news_url):

    detail_soup = get_soup(news_url,1)   # 构建beautifulsoup实例    
    news_detail = detail_soup.find("div", class_="article").decode()   
    import time
    time.sleep(0.5)  # 间隔时间防止反爬虫
    return news_detail

if __name__ == '__main__':

    
    feed_title = "首席经济学家论坛-首席文章"  # feed的标题，会显示在feed阅读器中
    feed_description = "首席经济学家论坛作为中国经济研究高端智囊的顶级思想平台 ，经济论坛立足于全球视角，着眼于中国经济增长和金融市场发展中的现实问题，促进首席经济学家间思想交流，向投资者传递研究信息，以求成为中国经济金融政策研究的高端咨询智囊。"  # feed的描述
    feed_name =  "chinacef.xml"  # feed xml文件的的名字
    website_url = 'https://www.chinacef.cn/#/article'  # 要爬取的页面
     
    feed_path = feeds_dir + feed_name
    feed_url = feeds_url + feed_name
    titles, contents, links, guids, updateds, publisheds = get_entrys(  feed_path)
    new_nums = 0
    old_nums = len(guids) 
    
    
    news_list = get_soup(website_url,1).find("div",class_="esslist").find_all("div",class_="list")
    
    news_list.reverse()  # 新的news排在列表后面  

    
    for news in news_list:
        news_url ="https://www.chinacef.cn/" +news.a.attrs['href']
        news_title = news.a.div.get_text()  # 新闻的标题
        guid = news_title

        if guid not in guids:             
            # news_title = news.a.div.get_text()  # 新闻的标题
            news_detail = get_content(news_url)  # 新闻详情
            
            
                      
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