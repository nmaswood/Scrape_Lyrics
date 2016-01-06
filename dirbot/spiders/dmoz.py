from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request

from dirbot.items import Website


class DmozSpider(Spider):

    name = "dmoz"
    start_urls = [
    "http://lyrics.wikia.com/wiki/Category:Genre"
    ]

    def parse(self, response):

        data =  response.xpath('//body//div[@id="mw-subcategories"]')

        urls = data.xpath("//td//a/@href").extract()

        for index, url in enumerate(urls):

            urls[index] = response.urljoin(url)

        for url in urls:

            yield Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):


        genre_text =  response.xpath("//body//div[@id='mw-pages']//h2//span//text()").extract()[0]
        genre = genre_text.split("Genre/")[-1].strip('"')

        artists = response.xpath('//body//div[@id="mw-pages"]//div[@class="mw-content-ltr"]')

        artists = artists.xpath('//tr//ul//li//a')


        for sel in artists:

            item = Website()
           
            url = sel.xpath('@href').extract()[0]
            url = response.urljoin(url)

            title = sel.xpath('@title').extract()[0]

            item['url'] = url
            item['title'] = title
            item['genre'] = genre
            
            yield item
