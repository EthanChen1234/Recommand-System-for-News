from scrapy import cmdline

# cmdline.execute('scrapy crawl sina1 -a page=3 -a flag=0'.split())  # 初始启动
cmdline.execute('scrapy crawl sina1 -a page=5 -a flag=1'.split())  # 0 全量， 1 增量
