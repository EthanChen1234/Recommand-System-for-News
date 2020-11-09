### 参考书籍
1. 《Python3网络开发爬虫实战》 ——崔庆才

### 代码注意事项
1. pipelines中设置存储的方式，存到数据库/csv
2. 在sina1中添加要爬取的url, 并需与域名、解析配套
3. settings中可以设置并发量等参数
4. 写入到MySQL中字段为'type', 'times', 'title', 'content'

### 启动文件
main.py

### 主要功能点
1. 支持爬全量、增量两种模式
2. 支持Selenium下拉功能


### windows 环境配置
conda create –n scrapy python=3.6.6
# 清华源写入到配置文件中
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

pip install scrapy==2.2.1
pip install selenium==3.141.0
pip install sqlalchemy==1.3.18
pip install pymysql==0.10.0
pip install pymongo == 3.11.0

# chromedriver配置
chromedriver下载地址 http://npm.taobao.org/mirrors/chromedriver/
chromedriver版本与chrome版本一致（帮助/关于Google Chrome/）, chrome更新chromedriver需对应更新
放入到浏览器安装位置和虚拟环境中：
C:\Users\Administrator\AppData\Local\Google\Chrome\Application
C:\SOFTWARES\anaconda3\envs\rs

