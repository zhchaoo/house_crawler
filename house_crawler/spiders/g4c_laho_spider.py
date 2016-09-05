import scrapy

from house_crawler import settings
from house_crawler.items import HouseItem

from scrapy.spidermiddlewares.httperror import HttpError
# from scrapy.shell import inspect_response


class G4cLahoSpider(scrapy.Spider):
    name = 'g4c_laho'
    download_delay = 2

    index_url = 'http://g4c.laho.gov.cn/search/clf/clfSearch.jsp'
    channel_name = settings.CHANNEL_NAME

    def __init__(self, max_pages=None, database_dir='./data', *args, **kwargs):
        super(G4cLahoSpider, self).__init__(*args, **kwargs)
        self.max_pages = max_pages
        self.start_urls = [self.index_url]
        self.database_dir = './data'

    def parse(self, response):
        # get max pages from response.
        if self.max_pages is None:
            self.max_pages = int(response.xpath('//table//select[@name="select"]/option/@value')[-1].extract())

        curr_page = 1
        while curr_page <= self.max_pages:
            yield scrapy.FormRequest(self.index_url,
                                     formdata={'channel_name': self.channel_name, 'currPage': str(curr_page)},
                                     callback=self.parse_page,
                                     errback=self.err_back)
            # enqueue next page
            curr_page += 1

    def parse_page(self, response):
        # inspect_response(response, self)

        curr_id = ''
        for table_row in \
                response.xpath('//td/a[contains(@href, "/search/clf/clf_detail.jsp?pyID=")]/parent::*/parent::*'):
            # parse items from page
            try:
                house_item = HouseItem()
                house_item["py_id"] = table_row.xpath('td/a/@href').re('\d+')[0]
                house_item["zone"] = table_row.xpath('td/a/text()')[1].extract()
                house_item["address"] = table_row.xpath('td/a/text()')[2].extract()
                house_item["total_price"] = float(table_row.xpath('td/a/text()')[3].extract())
                house_item["area_size"] = float(table_row.xpath('td/a/text()')[5].extract())
                house_item["date"] = table_row.xpath('td/a/text()')[8].extract()
                house_item["per_price"] = house_item["total_price"] / house_item["area_size"]
            except Exception as e:
                self.logger.error(repr(e))

            yield house_item

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


