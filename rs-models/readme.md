### 注意事项
1. MongoDB的可视化工具: NoSQL Manager for MongoDB Freeware
2. Redis可视化工具：Redis Desktop Manager


### step1 爬虫
1. scrapy\\sina\\main.py
2. 爬取数据到MySQL，定时任务（每天爬增量）


### step2 内容画像
1. models\\labels\\content_label.py
2. 处理 MySQL 中数据为内容画像，存到 MongoDB
3. 每10分钟做1次定时任务，热度值都是从10000开始，则会很大
4. MongoDB中的数据字段
    describe(原文), type, keywords(10个), word_num, news_date(新闻时间), 
    hot_heat(初始值10000), likes(点赞), reads(阅读), collections(收藏), create_time(处理时间)   


### step3 推荐列表
1. scheduler\\mongo_to_redis.py, 把MongoDB中的内容存到Redis中
   Redis中的字段：
        key："news_detail:"+content_id(MongoDB中唯一标识符),
        values: describe, type, news_date, content_id, likes, reads, collections, hot_heat
2. scheduler\\simple_res.py, 内容画像按时间顺序打分，存到Redis中
    value(content_id): score
    
                
                
### step4, 推荐系统工程化
andiord从后端取数据，并展示

flask 教程 w3c

postman 测试端口， "/recommendation/get_rec_list" （单元测试）

其它代码：注册/登录/点赞/收藏/获得点赞列表
把mongodb中的数据与代码联系起来
1）基于时间差更新MongoDB中的热度值
2）每次进来请求后，更新MongoDB中的热度值（热度增加）
3）牛顿冷却定律（热度下降）


下次课：
冷启动，热度召回
