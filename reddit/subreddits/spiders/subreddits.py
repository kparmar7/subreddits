import scrapy
import re
from ..items import SubredditsItem

class subredditsSpider(scrapy.Spider):
    name = "subreddits"
    start_urls = [
        "https://www.reddit.com/subreddits/"
    ]

    def parse(self, response):
        item = SubredditsItem()

        divEntry = response.css("div.entry")
        for entry in divEntry:
            title = entry.css('a.title::text').extract()
            comment = entry.css("div.md").extract()
            comment = re.sub('<[^>]+>', ' ', ' '.join(comment))
            comment = comment.replace("'\n              '", '')
            comment = comment.replace("\n", '')
            
            item['iTitle'] = title
            item['iComment'] = comment

            yield item

        next_page = response.css(".next-button a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page,  callback = self.parse)
