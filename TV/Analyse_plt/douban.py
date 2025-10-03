import pandas as pd
import jieba
import jieba.analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from snownlp import SnowNLP
import warnings

# 读取Excel文件
file_path = r'D:\AAAPycharmProjects\TV\douban_reviews.xlsx'
df = pd.read_excel(file_path)

# 提取评价文字和有用值
reviews = df['评价文字'].dropna()  # 去除空值
useful_values = df['有用值'].fillna(0)  # 将NaN替换为0

# 定义一个函数来过滤掉不需要的词语类型
def filter_words(word_freq, stop_words):
    filtered_freq = {word: freq for word, freq in word_freq.items() if word not in stop_words}
    return filtered_freq


# 加载自定义停用词表
with open(r'D:\AAAPycharmProjects\TV\stopwords.txt', 'r', encoding='utf-8') as f:
    stop_words = set(f.read().splitlines())

# 使用TextRank算法提取关键词，并结合情感分析
word_freq_dict = {}
for review, useful in zip(reviews, useful_values):
    s = SnowNLP(review)
    sentiment_score = s.sentiments  # 获取情感评分 [0, 1]，1表示积极，0表示消极

    # 提取关键词并加权
    keywords = jieba.analyse.textrank(review, topK=20, withWeight=True, allowPOS=('n', 'ns', 'nr', 'ng', 'v', 'vn'))
    for word, weight in keywords:
        if len(word.strip()) > 1:  # 只考虑长度大于1的词语
            if word in word_freq_dict:
                word_freq_dict[word] += (weight * int(useful) * (sentiment_score + 1))  # 加权，每个词至少计数一次
            else:
                word_freq_dict[word] = (weight * int(useful) * (sentiment_score + 1))

# 过滤掉不需要的词语
filtered_word_freq = filter_words(word_freq_dict, stop_words)

# 生成词云
wordcloud = WordCloud(
    font_path='simhei.ttf',  # 设置字体路径，以支持中文
    width=800,
    height=400,
    background_color='white',
    max_words=200
).generate_from_frequencies(filtered_word_freq)

# 设置matplotlib的全局字体为支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 忽略字体相关的警告
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

# 保存并显示词云图
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # 不显示坐标轴
plt.title('电视剧评论词云')
plt.savefig('wordcloud.png', bbox_inches='tight', dpi=300)  # 保存为PNG文件
plt.show()

# 绘制评分分布直方图
ratings = df['评价分数'].dropna()  # 假设评分列名为'评价分数'

plt.figure(figsize=(10, 5))
plt.hist(ratings, bins=10, edgecolor='black', alpha=0.7)
plt.xlabel('评分')
plt.ylabel('频数')
plt.title('电视剧评分分布')
plt.grid(True)
plt.savefig('rating_histogram.png', bbox_inches='tight', dpi=300)  # 保存为PNG文件
plt.show()

# 输出有用值最高的前五条评论
top_reviews = df.nlargest(5, '有用值')[['评价文字', '有用值']]
print("有用值最高的前五条评论：")
for index, row in top_reviews.iterrows():
    print(f"有用值: {row['有用值']}, 评价: {row['评价文字']}")