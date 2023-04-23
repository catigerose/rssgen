
1. rss介绍：https://cyber.harvard.edu/rss/
2. atom介绍：https://validator.w3.org/feed/docs/atom.html
3. feed本质是一个xml文件，不但符合xml格式要求，另外需要满足feed的协议要求。
4. feed订阅链接本质上是一个  feed xml文件的 URl。一般通过搭建http服务器实现。
5. feed xml文件会定时改变其内容，rss客户端定时抓取保存，以实现“推送消息”的功能。
6. feed 生成器 的作用就是 修改、更新xml文件
7. feed服务器定时获取feed的更新内容，并保存。 该服务器可以是本地客户端、服务器提高商如inoreader，或自行搭建的RSS服务如freshrss。云端的rss服务可以实现24小时抓取，自行设定更新时间，inoreader免费版无法定制更新时间，本地客户端如不24小时后台运行，可能会漏掉信息。

 







