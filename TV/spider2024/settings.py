# spider2024/settings.py
BOT_NAME = 'spider2024'

SPIDER_MODULES = ['spider2024.spiders']
NEWSPIDER_MODULE = 'spider2024.spiders'

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
   'spider2024.pipelines.ExcelPipeline': 300,
}

# 设置下载延迟，单位为秒，这里是2秒
DOWNLOAD_DELAY = 2

# 启用自动限速扩展
AUTOTHROTTLE_ENABLED = True
# 初始下载延迟
AUTOTHROTTLE_START_DELAY = 5
# 最大下载延迟
AUTOTHROTTLE_MAX_DELAY = 60
# 自动限速的调试模式
AUTOTHROTTLE_DEBUG = False

# 启用Cookies (豆瓣需要登录状态)
COOKIES_ENABLED = True

# 并发请求数量限制
CONCURRENT_REQUESTS = 16
# 对单个域名的并发请求数量限制
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# 随机User-Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# 启用日志记录
LOG_LEVEL = 'INFO'



DOWNLOADER_MIDDLEWARES = {
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # 禁用默认的User-Agent中间件
    'spider2024.middlewares.CustomRetryMiddleware': 543,  # 自定义403重试中间件
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,  # 禁用默认的重试中间件
}
