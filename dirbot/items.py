from scrapy.item import Item, Field


class Website(Item):

    url = Field()
    genre = Field()
    title = Field()

