import re
import scrapy
from scrapy import Request
from news163.items import News163Item
import requests


class TechnewsSpider(scrapy.Spider):
    name = 'technews'
    start_url = 'http://tech.163.com/special/00097UHL/tech_datalist{}.js?callback=data_callback'
    # 热点api；http://temp.163.com/special/00804KVA/cm_yaowen{}.js?callback=data_callback
    # 财经api：http://money.163.com/special/002557S5/newsdata_idx_licai{}.js?callback=data_callback
    # 体育api：http://sports.163.com/special/000587PR/newsdata_n_index{}.js?callback=data_callback
    # 娱乐api：http://ent.163.com/special/000380VU/ent_photoview_api{}.js?callback=data_callback

    def start_requests(self):
        n = 2
        yield Request(url=self.start_url.format(''), callback=self.parse_index)
        while requests.get(url=self.start_url.format('_0'+str(n))).status_code == 200:
            yield Request(url=self.start_url.format('_0'+str(n)), callback=self.parse_index)
            n = n + 1

    def parse_index(self, response):
        resp = response.text
        result = eval(resp.replace('data_callback', ''))

        for i in result:
            if i.get('docurl') and re.match('http://tech.163.com/17/0630', i.get('docurl')):
                yield Request(i.get('docurl'), callback=self.parse_detial)


    def parse_detial(self, response):
        items = News163Item()
        title = response.xpath('//h1/text()').extract_first()
        post_time, post_source = ''.join(response.xpath('//div[@class="post_time_source"]//text()').extract()).strip().replace('\n', '').replace('\u3000', '').split('来源:')
        contents = ''.join(response.xpath('//div[@class="post_text"]//p//text()').extract()).strip().replace('\n', '')
        ep_editor = response.xpath('//span[@class="ep-editor"]/text()').extract_first()
        # post_comment_tiecount = response.xpath('//div[@class="post_comment_tiecount"]/a/text()').extract_first(default=None)
        # post_comment_joincount = response.xpath('//div[@class="post_comment_joincount"]/a/text()').extract_first(default=None)

        for field in items.fields:
            items[field] = eval(field)
        yield items








