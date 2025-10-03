import scrapy
from scrapy import Selector, Request
from spider2024.items import TVCommentItem
import random
import logging
from scrapy.downloadermiddlewares.retry import RetryMiddleware

# User-Agent列表
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
]


def get_random_user_agent():
    return random.choice(USER_AGENTS)


class DoubanSpider(scrapy.Spider):
    name = 'douban_reviews'
    allowed_domains = ['douban.com']
    start_urls = [
        "https://movie.douban.com/subject/26727273/comments?start=0&limit=20&status=P&sort=new_score"
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'RETRY_ENABLED': True,  # 启用重试机制
        'RETRY_TIMES': 3,  # 重试次数
        'LOG_LEVEL': 'INFO',  # 设置日志级别
        'COOKIES_ENABLED': True,  # 启用Cookies
        'USER_AGENT': get_random_user_agent(),  # 使用随机User-Agent
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
        }
    }

    def start_requests(self):
        # 提供的完整Cookie字符串
        cookie_string = (
            'bid=qSDPpZ5oVkM; '
            'll="108309"; '
            '_vwo_uuid_v2=D19B2F9074AF1A47648D9D2C89C19B489|2c3d4d9a8d339718e01a39b19c0665b4; '
            'push_noty_num=0; '
            'push_doumail_num=0; '
            '__utmv=30149280.21125; '
            'dbcl2="211258079:2rplLkNu+fo"; '
            '__utmz=30149280.1735519053.10.6.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; '
            'Hm_lvt_6d4a8cfea88fa457c3127e14fb5fabc2=1735520408; '
            '_gid=GA1.2.534935106.1735743847; '
            '_ga=GA1.2.2017050372.1735520409; '
            '_ga_Y4GN1R87RG=GS1.1.1735743847.2.1.1735745073.0.0.0; '
            'ck=l7eA; '
            'ap_v=0,6.0; '
            '__utma=30149280.272153819.1730449627.1735743816.1735785625.13; '
            '__utmb=30149280.0.10.1735785625; '
            '__utmc=30149280; '
            'frodotk="60578f79af57ba1e2106ae6d0e072e5a"; '
            'talionusr="eyJpZCI6ICIyMTEyNTgwNzkiLCAibmFtZSI6ICJCbHVlIENhdCBCbHVlcyJ9"'
        )

        # 将Cookie字符串转换为字典
        cookies = {cookie.split('=')[0]: cookie.split('=', 1)[1] for cookie in cookie_string.split('; ')}

        headers = {
            'User-Agent': get_random_user_agent()  # 随机选择User-Agent
        }

        for url in self.start_urls:
            yield Request(
                url=url,
                headers=headers,
                cookies=cookies,  # 添加完整的Cookie
                callback=self.parse_reviews,
                meta={'start': 0, 'dont_merge_cookies': False},  # 传递当前的start参数并允许合并Cookies
                errback=self.handle_error  # 错误回调函数
            )

    def parse_reviews(self, response):
        sel = Selector(response)

        reviews = sel.css("#comments > div.comment-item")
        for review in reviews:
            review_item = TVCommentItem()

            # 提取评分标题
            rating_title = review.css("span.rating::attr(title)").get()
            if rating_title:
                review_item['rating'] = rating_title
            else:
                review_item['rating'] = None  # 如果没有评分，则设置为None

            # 提取评论文本
            review_text = review.css("span.short::text").get()
            if review_text:
                review_item['review_text'] = review_text.strip()
            else:
                review_item['review_text'] = None  # 如果没有评论文本，则设置为None

            # 提取有用计数
            useful_count = review.css("span.votes::text").get()
            if useful_count:
                review_item['useful_count'] = useful_count
            else:
                review_item['useful_count'] = None  # 如果没有有用计数，则设置为None

            logging.info(f"Extracted review: {review_item}")
            yield review_item

        # 获取当前页的start参数
        current_start = response.meta.get('start', 0)

        # 构造下一页的URL
        next_start = current_start + 20
        next_page_url = f"https://movie.douban.com/subject/26727273/comments?start={next_start}&limit=20&status=P&sort=new_score"

        # 检查是否有更多评论
        if len(reviews) == 20:  # 如果当前页有20条评论，说明还有下一页
            logging.info(f"Next page URL: {next_page_url}")
            yield Request(
                url=next_page_url,
                headers=response.request.headers,
                cookies=response.request.cookies,  # 传递当前请求的Cookie
                callback=self.parse_reviews,
                meta={'start': next_start, 'dont_merge_cookies': False},  # 传递下一页的start参数并允许合并Cookies
                dont_filter=True,  # 确保不会因为重复URL而被过滤
                errback=self.handle_error  # 错误回调函数
            )
        else:
            logging.info("No more comments to fetch.")  # 如果当前页少于20条评论，说明已经到达最后一页

    def handle_error(self, failure):
        """处理请求失败的情况"""
        self.logger.error(f"Request failed on {failure.request.url}: {failure.value}")
        # 这里可以根据需要决定是否重新调度请求
        # 例如：return Request(url=failure.request.url, callback=self.parse_reviews, dont_filter=True)