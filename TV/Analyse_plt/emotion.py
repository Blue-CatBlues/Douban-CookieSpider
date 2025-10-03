import pandas as pd
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import seaborn as sns

# 读取 Excel 文件
file_path = r'D:\AAAPycharmProjects\TV\douban_reviews.xlsx'
df = pd.read_excel(file_path)

# 预处理文本（去除特殊字符等）
def preprocess_text(text):
    if isinstance(text, str):  # 确保文本是字符串类型
        return text.strip().lower()
    return ''  # 如果不是字符串，返回空字符串

df['评价文字'] = df['评价文字'].apply(preprocess_text)

# 情感分析
def get_detailed_sentiment(text):
    if not text:  # 如果文本为空，返回中立
        return '中立'

    s = SnowNLP(text)
    sentiment_score = s.sentiments  # 获取情感得分，范围为 [0, 1]

    if sentiment_score >= 0.9:
        return '非常积极'
    elif sentiment_score >= 0.7:
        return '积极'
    elif sentiment_score > 0.4 and sentiment_score < 0.6:
        return '中立'
    elif sentiment_score <= 0.3:
        return '非常消极'
    elif sentiment_score <= 0.6:
        return '消极'
    else:
        return '中立'

# 应用细化后的情感分析函数
df['detailed_sentiment'] = df['评价文字'].apply(get_detailed_sentiment)

# 统计每种情感的评论数
detailed_sentiment_counts = df['detailed_sentiment'].value_counts()

# 计算总评论数
total_reviews = df.shape[0]

# 统计每种情感的评论数并计算比例
detailed_sentiment_proportions = detailed_sentiment_counts / total_reviews

# 打印比例
print("情感类别比例：")
print(detailed_sentiment_proportions)

# 设置中文字体以避免中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# 创建饼图
plt.figure(figsize=(8, 8))
plt.pie(detailed_sentiment_counts, labels=detailed_sentiment_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
plt.title('电视剧评论情感分布')
plt.axis('equal')  # 保持饼图为圆形
plt.show()

# 创建条形图
plt.figure(figsize=(10, 6))
sns.barplot(x=detailed_sentiment_counts.values,
            y=detailed_sentiment_counts.index,
            palette='viridis',
            hue=detailed_sentiment_counts.index,
            dodge=False, legend=False)
plt.title('不同情感类别的评论数量')
plt.xlabel('评论数量')
plt.ylabel('情感类别')
plt.grid(True)
plt.show()

# 保存图表
plt.savefig('sentiment_pie_chart.png', bbox_inches='tight', dpi=300)  # 保存饼图