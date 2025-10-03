import openpyxl
from itemadapter import ItemAdapter
from spider2024.items import TVCommentItem


class ExcelPipeline:
    def open_spider(self, spider):
        # 当爬虫开启时调用此方法，创建一个新的 Excel 工作簿
        self.wb = openpyxl.Workbook()
        self.sheet = self.wb.active
        self.sheet.title = "Reviews"
        self.sheet.append(['评价分数', '评价文字', '有用值'])
        spider.logger.info("Excel 文件已创建")

    def close_spider(self, spider):
        self.wb.save(r"D:\AAAPycharmProjects\douban_reviews.xlsx")  # 保存为一个文件
        spider.logger.info("Excel 文件已保存")

    def process_item(self, item, spider):
        if isinstance(item, TVCommentItem):
            self.sheet.append([
                item['rating'],
                item['review_text'],
                item['useful_count']
            ])
            spider.logger.info(f"处理评论项目: {item['useful_count']}, "
                               f"{item['rating']}, {item['review_text'][:50]}...")

        return item
