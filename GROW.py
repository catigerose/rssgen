from feed_funcs import get_soup, gen_fg, feeds_url, feeds_dir, get_entrys, tz
from datetime import datetime

if __name__ == '__main__':

    
    feed_title = "思睿研究"  # feed的标题，会显示在feed阅读器中
    feed_description = "思策为君 睿赢未来"  # feed的描述
    feed_name =  "GROW.xml"  # feed xml文件的的名字
    website_url = 'https://growinvestment.group/home-2/'  # 要爬取的页面
     
    feed_path = feeds_dir + feed_name
    feed_url = feeds_url + feed_name
    titles, contents, links, guids, updateds, publisheds = get_entrys(  feed_path)
    new_nums = 0
    old_nums = len(guids) 
    
    
    news_list = get_soup('https://growinvestment.group/home-2/').find("main",id="main").find_all("article")
    
    news_list.reverse()  # 新的news排在列表后面  
    for news in news_list:
        news_url =news.header.h2.a.attrs['href']
        guid = news_url

        if guid not in guids:             
            news_title = news.header.h2.a.get_text()  # 新闻的标题
            news_detail = news.div.ul.find_all("li")[0].get_text()  
            for li in news.div.ul.find_all("li"):
                news_detail +=  "\n"
                news_detail +=  li.get_text()  

            
                      
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