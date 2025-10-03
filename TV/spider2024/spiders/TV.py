import scrapy
from scrapy import Selector
from spider2024.items import tv_Item
import json
from datetime import datetime
class ActorSpider(scrapy.Spider):
    name = "TV"
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
            "#J-lemma-main-wrapper > div > div > div > div > div > div:nth-child(74) > div > table > tbody > tr")
        self.log(f"找到了 {len(list_items)} items")

        items = []
        for list_item in list_items:
            item = tv_Item()
            item["num"] = list_item.css("td:nth-child(2) > div > span::text").get()
            print(item["num"])
            item["date"] = list_item.css("td:nth-child(1) > div > span::text").get()
            print(item["date"])
            item["city_tv"] = list_item.css("td:nth-child(3) > div > span::text").get()
            print(item["city_tv"])
            item["city_tv_per"] = list_item.css("td:nth-child(4) > div > span::text").get()
            print(item["city_tv_per"])
            item["china_tv"] = list_item.css("td:nth-child(6) > div > span::text").get()
            print(item["num"])
            item["china_tv_per"] = list_item.css("td:nth-child(7) > div > span::text").get()
            print(item["num"])
            if not item["date"]:
                continue  # 如果日期为空，跳过此行

            try:
                # 尝试将日期字符串解析为 datetime 对象，格式为 "YYYY.M.D"
                date_obj = datetime.strptime(item["date"].strip(), "%Y.%m.%d")
                item["date"] = item["date"].strip()  # 保存原始日期字符串
                print(f"提取到的日期是{date_obj}")
            except ValueError:
                self.log(f"无效的日期格式: {item["date"]}")
                continue  # 如果日期格式无效，跳过此行

            # 只将日期有效的项添加到 items 列表中
            if item["date"]:
                items.append(dict(item))

        # 将数据写入 JSON 文件，确保以 UTF-8 编码保存
        with open('D:\\AAAPycharmProjects\\TV\\TV_info.json', 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)  # 使用 ensure_ascii=False
        self.log("数据已写入 TV_info.json 文件")