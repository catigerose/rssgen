# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 12:00:33 2023

@author: catig
"""
from feed_funcs import get_soup, gen_fg, feeds_url, feeds_dir, get_entrys, tz
from datetime import datetime

ths_id = "231729/"
domain = " http://t.10jqka.com.cn/circle/"
website_url =domain+ths_id


soup = get_soup(website_url,1).find(
    "ul", class_="postlist-ul").find_all("li",class_="post-single clearfix") 
print(soup[0])
print(soup[2])
print(soup[1])