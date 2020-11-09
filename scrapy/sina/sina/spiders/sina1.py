import scrapy
from selenium import webdriver
from scrapy.http import Request
from sina.items import DataItem
from scrapy.selector import Selector


import datetime
import re


class Sina1Spider(scrapy.Spider):
    name = 'sina1'
    allowed_domains = ['sina.com.cn']

    def __init__(self, page=None, flag=None, *args, **kwargs):
        super(Sina1Spider, self).__init__(*args, **kwargs)
        self.page = int(page)
        self.flag = int(flag)  # 0, 全量， 1，增量
        # self.start_urls = ['https://ent.sina.com.cn/zongyi/']  # Linux
        self.start_urls = ['https://ent.sina.com.cn/film/',
                           'https://ent.sina.com.cn/zongyi/',
                           'https://news.sina.com.cn/china/']
        self.option = webdriver.ChromeOptions()
        # 不打开网页
        self.option.add_argument('headless')
        # 没沙河
        self.option.add_argument('no-sandbox')
        # 设置不爬取图片图片
        self.option.add_argument('--blink-setting=imagesEnabled=false')

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        driver = webdriver.Chrome(chrome_options=self.option)
        driver.set_page_load_timeout(30)
        driver.get(response.url)
        for i in range(self.page):
            # 查找是否有下一页
            while not driver.find_element_by_xpath("//div[@class='feed-card-page']").text:
                # 没有就进行滑动
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            title = driver.find_elements_by_xpath("//h2[@class='undefined']/a[@target='_blank']")  # 取不到 "组图", "热"
            time = driver.find_elements_by_xpath("//h2[@class='undefined']/../div[@class='feed-card-a feed-card-clearfix']/div[@class='feed-card-time']")
            for i in range(len(title)):
                eachtitle = title[i].text
                eachtime = time[i].text
                item = DataItem()
                if response.url == "https://ent.sina.com.cn/zongyi/":
                    item['type'] = 'zongyi'
                elif response.url == 'https://news.sina.com.cn/china/':
                    item['type'] = 'china'
                else:
                    item['type'] = 'film'
                item['title'] = eachtitle
                item['desc'] = ''
                href = title[i].get_attribute('href')
                today = datetime.datetime.now()
                # 今天08:14， 9月1日 16:56，2020年 8月31日 10:46，4分钟前,
                eachtime = eachtime.replace('今天', str(today.month)+'月'+str(today.day) + '日')
                if '分钟前' in eachtime:
                    minute = int(eachtime.split('分钟前')[0])
                    t = datetime.datetime.now() - datetime.timedelta(minutes=minute)
                    t2 = datetime.datetime(year=t.year, month=t.month, day=t.day, hour=t.hour, minute=t.minute)
                else:
                    if '年' not in eachtime:
                        eachtime = str(today.year) + '年' + eachtime
                    t1 = re.split(r'[年月日:]', eachtime)
                    t2 = datetime.datetime(year=int(t1[0]), month=int(t1[1]), day=int(t1[2]), hour=int(t1[3]),
                                           minute=int(t1[4]))

                item['times'] = t2

                if self.flag == 1:
                    today = datetime.datetime.now().strftime("%Y-%m-%d")
                    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                    if item['times'].strftime("%Y-%m-%d") < yesterday:
                        driver.close()
                        break
                    if yesterday <= item["times"].strftime("%Y-%m-%d") < today:  # 只取前一天的消息
                        yield Request(url=response.urljoin(href), meta={'name': item}, callback=self.parse_decription)

                else:
                    yield Request(url=response.urljoin(href), meta={'name': item}, callback=self.parse_decription)
            try:
                driver.find_element_by_xpath("//div[@class='feed-card-page']/span[@class='pagebox_next']/a").click()
            except:
                break

    def parse_decription(self, response):
        selector = Selector(response)
        desc = selector.xpath("//div[@class='article']/p/text()").extract()
        item = response.meta['name']
        desc = list(map(str.strip,desc))
        item['desc'] = ''.join(desc)
        yield item




