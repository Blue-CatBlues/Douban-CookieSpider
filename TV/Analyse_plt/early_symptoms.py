import json
import matplotlib.pyplot as plt
from datetime import datetime
import re  # 导入正则表达式模块
import matplotlib.font_manager as fm

# 设置中文字体以避免中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号'-'显示为方块的问题

# 假设数据文件名为actors_info.json，路径根据实际情况调整
file_path = r"D:\AAAPycharmProjects\TV\actors_info.json"
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

male_ages = []
male_bmis = []
female_ages = []
female_bmis = []

for item in data:
    if all(k in item for k in ('birth_day', 'height', 'weight', 'sex')):
        # 处理出生日期
        birth_day_str = item['birth_day']
        for date_format in ['%Y年%m月%d日', '%Y-%m-%d', '%Y/%m/%d']:
            try:
                birth_day = datetime.strptime(birth_day_str, date_format)
                break
            except ValueError:
                continue
        else:  # 如果所有格式都不匹配
            print(f"无法解析出生日期: {birth_day_str}")
            continue

        age = datetime.now().year - birth_day.year

        # 处理身高
        height_str = item['height'].strip().lower()
        match = re.match(r"(\d+(\.\d+)?)", height_str)
        if not match:
            print(f"无法解析身高数据: {height_str}")
            continue
        height_num = float(match.group(1))
        if height_str.endswith('cm'):
            height = height_num / 100  # 将厘米转换为米
        elif height_str.endswith('m'):
            height = height_num
        else:
            print(f"未知的身高单位: {height_str}")
            continue

        # 处理体重
        weight_str = item['weight'].strip().lower()
        match = re.match(r"(\d+(\.\d+)?)", weight_str)
        if not match:
            print(f"无法解析体重数据: {weight_str}")
            continue
        weight = float(match.group(1))

        # 计算BMI
        bmi = weight / (height ** 2)

        # 分类存储
        if item['sex'] == '男':
            male_ages.append(age)
            male_bmis.append(bmi)
        elif item['sex'] == '女':
            female_ages.append(age)
            female_bmis.append(bmi)

# 绘制散点图
plt.figure(figsize=(10, 6))
plt.scatter(male_ages, male_bmis, label='男性', c='blue', alpha=0.9)
plt.scatter(female_ages, female_bmis, label='女性', c='red', alpha=1)

# 添加标题和坐标轴标签
plt.title('男女演职人员BMI对比分析图')
plt.xlabel('年  龄')
plt.ylabel('BMI')

# 添加图例
plt.legend()

# 显示图形
plt.grid(True)  # 添加网格线
plt.show()