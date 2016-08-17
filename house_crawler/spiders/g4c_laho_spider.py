import scrapy

from house_crawler import settings
from house_crawler.items import HouseItem

from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.shell import inspect_response

class G4cLahoSpider(scrapy.Spider):
    name = 'g4c_laho'
    download_delay = 2


    index_url = 'http://g4c.laho.gov.cn/search/clf/clfSearch.jsp'
    max_page_limit = 100
    chnlname = settings.CHNL_NAME

    def start_requests(self):
        curr_page = 1
        while curr_page < self.max_page_limit:
            yield scrapy.FormRequest(self.index_url,
                                 formdata={ 'chnlname' : self.chnlname, 'currPage': str(curr_page) },
                                 callback=self.parse,
                                 errback=self.err_back)
            # enqueue next page
            curr_page += 1

    def parse(self, response):
        curr_id = ''
        for table_row in \
                response.xpath('//td/a[contains(@href, "/search/clf/clf_detail.jsp?pyID=")]/parent::*/parent::*'):

            house_item = HouseItem()
            house_item["py_id"] = table_row.xpath('td/a/@href').re('\d+')[0]
            house_item["zone"] = table_row.xpath('td/a/text()')[1].extract()
            house_item["address"] = table_row.xpath('td/a/text()')[2].extract()
            house_item["total_price"] = float(table_row.xpath('td/a/text()')[3].extract())
            house_item["area_size"] = float(table_row.xpath('td/a/text()')[5].extract())
            house_item["per_price"] = house_item["total_price"] / house_item["area_size"]

            yield house_item



    def parse_item(self, table_row):
        item = HouseItem()
        yield item

    def err_back(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)


