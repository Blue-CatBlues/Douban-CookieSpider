import scrapy


class actor_Item(scrapy.Item):
    name = scrapy.Field()
    sex = scrapy.Field()
    nation = scrapy.Field()
    birth_day = scrapy.Field()
    constellation = scrapy.Field()
    blood_type = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()


class actor_link(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()


class tv_Item(scrapy.Item):
    num = scrapy.Field()
    date = scrapy.Field()
    city_tv = scrapy.Field()
    china_tv = scrapy.Field()
    city_tv_per = scrapy.Field()
    china_tv_per = scrapy.Field() 


class TVCommentItem(scrapy.Item):
    rating = scrapy.Field()       # 评价分数
    review_text = scrapy.Field()  # 评价文字
    useful_count = scrapy.Field()  # 有用值
