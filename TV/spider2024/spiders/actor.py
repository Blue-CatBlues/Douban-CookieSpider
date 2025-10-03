import scrapy
from scrapy import Selector
from spider2024.items import actor_link
import json

class ActorSpider(scrapy.Spider):
    name = 'ActorLink'
    allowed_domains = ['baike.baidu.com']
    start_urls = [
        'https://baike.baidu.com/item/%E4%BA%BA%E6%B0%91%E7%9A%84%E5%90%8D%E4%B9%89/17545218#9-1']

    custom_settings = {
        'DOWNLOAD_DELAY': 0,  # 没有延迟
        'CONCURRENT_REQUESTS': 32,  # 增加并发请求数量
        'AUTOTHROTTLE_ENABLED': False,  # 禁用自动限速
    }
    
    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers)

    def parse(self, response):
        self.log(f"Response status: {response.status}")
        self.log(f"Response body: {response.text[:600]}")

        sel = Selector(response)
        list_items = sel.css(
            "#J-lemma-main-wrapper > div > div > div> div > div > div:nth-child(11) > div > div > div > div > div > div")
        self.log(f"找到了 {len(list_items)} items")

        items = []
        for list_item in list_items:
            actor_item = actor_link()
            actor_item["name"] = list_item.css("dl > dt > span:nth-child(1) > a::text").get()
            print(actor_item["name"])
            actor_item["link"] = response.urljoin(list_item.css("dl > dt > span:nth-child(1) > a::attr(href)").get())
            print(actor_item["link"])
            # 只将 name 不为 null 的项添加到 items 列表中
            if actor_item["name"] is not None:
                items.append(dict(actor_item))

        # 将数据写入 JSON 文件，确保以 UTF-8 编码保存
        with open('D:\\AAAPycharmProjects\\TV\\actors_link.json', 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)  # 使用 ensure_ascii=False
        self.log("数据已写入到 D:\\AAAPycharmProjects\\TV\\Actor_link.json 文件")