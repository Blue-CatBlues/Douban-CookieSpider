import scrapy
from spider2024.items import actor_Item
import json
from scrapy import Selector

class ActorDetailSpider(scrapy.Spider):
    name = 'ActorDetail'
    allowed_domains = ['baike.baidu.com']
    actor_infos = []  # 将 actor_infos 集合放在类的属性中

    custom_settings = {
        'DOWNLOAD_DELAY': 0,  # 没有延迟
        'CONCURRENT_REQUESTS': 32,  # 增加并发请求数量
        'AUTOTHROTTLE_ENABLED': False,  # 禁用自动限速
    }
    
    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
        }
        # 读取 JSON 文件中的链接
        with open('actors_link.json', 'r', encoding='utf-8') as f:
            actor_links = json.load(f)

        for actor in actor_links:
            url = actor['link']
            self.log(f"找到了这个链接: {url}")
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):
        sel = Selector(response)
        temp_part = sel.css("#J-lemma-main-wrapper > div > div > div > div > div > dl > div")
        print(f'找到了 {len(temp_part)} 个属性')


        item = actor_Item()

        for part in temp_part:
            if part.css("dt::text").get() == "本\xa0\xa0\xa0\xa0名":
                item['name'] = part.css('dd > span::text').get()
                print(f"本\xa0\xa0\xa0\xa0名: {item['name']}")
            if part.css("dt::text").get() == "性\xa0\xa0\xa0\xa0别":
                item['sex'] = part.css('dd > span::text').get()
                print(f"性\xa0\xa0\xa0\xa0别: {item['sex']}")
            if part.css("dt::text").get() == "民\xa0\xa0\xa0\xa0族":
                item['nation'] = part.css('dd > span::text').get()
                print(f"民\xa0\xa0\xa0\xa0族: {item['nation']}")
            if part.css("dt::text").get() == "出生日期":
                item['birth_day'] = part.css('dd > span ::text').get()
                print(f"出生日期: {item['birth_day']}")
            if part.css("dt::text").get() == "星\xa0\xa0\xa0\xa0座":
                item['constellation'] = part.css('dd > span > a::text').get()
                print(f"星\xa0\xa0\xa0\xa0座: {item['constellation']}")
            if part.css("dt::text").get() == "血\xa0\xa0\xa0\xa0型":
                item['blood_type'] = part.css('dd > span::text').get()
                print(f"血\xa0\xa0\xa0\xa0型: {item['blood_type']}")
            if part.css("dt::text").get() == "身\xa0\xa0\xa0\xa0高":
                item['height'] = part.css('dd > span::text').get()
                print(f"身\xa0\xa0\xa0\xa0高: {item['height']}")
            if part.css("dt::text").get() == "体\xa0\xa0\xa0\xa0重":
                item['weight'] = part.css('dd > span::text').get()
                print(f"体\xa0\xa0\xa0\xa0重: {item['weight']}")

        self.actor_infos.append(dict(item))

        yield item

    def closed(self, reason):
        # 在爬虫结束时将结果保存到 JSON 文件中
        with open('D:\\AAAPycharmProjects\\TV\\actors_info.json', 'w', encoding='utf-8') as f:
            json.dump(self.actor_infos, f, ensure_ascii=False, indent=4)
