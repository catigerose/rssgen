from feed_funcs import get_soup, gen_fg, feeds_url, feeds_dir, get_entrys, tz
from datetime import datetime
import time

# 该函数获取详情页的新闻内容
def get_content(news_url):
    urls = [news_url]
    content = ""
    soup = get_soup(news_url)
    if soup.find("div","pagenavbar"):
        othter_pages = soup.find("div","pagenavbar").find_all("span")[1:-1]
        for page in othter_pages:
            urls.append(website_url+page.a.attrs['href'])
        
        for url in urls:
            soup = get_soup(url)
            soup.find("div","newsText fix").find("div",class_="pagenavbar").decompose()
            soup.find("div","newsText fix").find_all("strong")[-1].decompose()
            soup.find("div","newsText fix").find_all("div")[-1].decompose()
            content += soup.find("div","newsText fix").decode()
    else:
        for url in urls:
            soup = get_soup(url)
            time.sleep(2)
            #soup.find("div","newsText fix").find("div",class_="pagenavbar").decompose()
            soup.find("div","newsText fix").find_all("strong")[-1].decompose()
            #soup.find("div","newsText fix").find_all("div")[-1].decompose()
            content += soup.find("div","newsText fix").decode()
 
   
    time.sleep(2)  # 间隔时间防止反爬虫
    return content

if __name__ == '__main__':

    feed_title = "日经中文网"  # feed的标题，会显示在feed阅读器中
    feed_description = "日经中文网官方网站。日经中文网是日本经济新闻社的中文财经网站。提供日本、中国、欧美财经金融信息、商务、企业、高科技报道、评论和专栏。"  # feed的描述
    feed_name = "nikkei.xml"  # feed xml文件的的名字
    website_url = 'https://cn.nikkei.com'  # 要爬取的页面
    
    feed_path = feeds_dir + feed_name
    feed_url = feeds_url + feed_name
    titles, contents, links, guids, updateds, publisheds = get_entrys(  feed_path)
    new_nums = 0
    old_nums = len(guids) 
    
   
    
    soup = get_soup(website_url)
    soup = soup.find("div",class_="column-2 mainContent")   #左侧新闻
    
    news_list =[]  #用于汇集所有新闻
    
    news_list.append(soup.find("div",class_="indexTopNews fix mB5").find("dl",class_="newsContent01").find("dt")) #top news第一个新闻
    
    top_news = soup.find("div",class_="indexTopNews fix mB5").find("dl",class_="newsContent01").find("ul").find_all("li")   
    news_list.extend(top_news) #top news
    
    focus = soup.find("div",class_="fix pR15").find("div",class_="column-1 frt").find_all("dl",class_="newsContent01")[0].find_all("dt")
    news_list.extend(focus)  #聚焦板块
    
    column = soup.find("div",class_="fix pR15").find("div",class_="column-1 frt").find_all("dl",class_="newsContent01")[1].find_all("dt")
    news_list.extend(column)  #专栏板块
    
   
    
    
    news_list.reverse()  # 新的news排在列表后面  
    for news in news_list:
        news_url = website_url+news.a.attrs['href']  # 详情页的url
        guid = news_url


        if guid not in guids:             
            news_title = news.a.get_text()  # 新闻的标题
            news_detail = get_content(news_url)
            
                      
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
