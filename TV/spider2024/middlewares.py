from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import logging


class CustomRetryMiddleware(RetryMiddleware):
    def process_response(self, request, response, spider):
        return super().process_response(request, response, spider)