import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

# 设置全局字体为雅黑，增强图表中文显示效果
plt.rcParams['font.family'] = ['Microsoft YaHei']
# 设置全局轴标签字号大小，使图表标签显示更清晰
plt.rcParams['axes.labelsize'] = 14

# 1. 读取数据
with open('new_TV_info.json', 'r') as file:
    data = json.load(file)

# 将数据转换为DataFrame格式，方便后续处理
df = pd.DataFrame(data)
# 将相关字段转换为合适的数据类型，比如数值型
df['city_tv_per'] = df['city_tv_per'].astype(float)
df['num'] = df['num'].astype(int)
# 这里为了示例简单，把日期字符串拆分成年、月、日三列
df['year'], df['month'], df['day'] = df['date'].str.split('.', expand=True).astype(int)

# 2. 准备特征和目标变量
X = df[['num', 'year', 'month', 'day']]  # 特征，可以按需增加更多特征
y = df['city_tv_per']  # 目标变量（这里修改为CSM52城市网收视份额%）

# 3. 划分训练集和测试集
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. 构建随机森林回归模型并训练
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)  # 可调整参数
rf_model.fit(X_train, y_train)

# 5. 在测试集上进行预测
y_pred = rf_model.predict(X_test)

# 6. 可视化呈现（绘制预测值和真实值对比图）
plt.scatter(X_test['num'], y_test, label='真实值')
plt.scatter(X_test['num'], y_pred, label='预测值')
plt.xlabel('集数')
plt.ylabel('收视份额(%)')  # 修改ylabel为收视份额(%)
plt.title('2025年类似《人民的名义》电视剧收视份额预测值和真实值对比')
plt.legend()
plt.savefig("2025年类似《人民的名义》电视剧收视份额预测值和真实值对比")
plt.show()

# 7. 对于2025年的预测
future_df = pd.DataFrame()
# 假设集数从1到假设的30集
future_df['num'] = np.arange(1, 31)
future_df['year'] = 2025
future_df['month'] = 1
future_df['day'] = np.arange(1, 31)
future_predictions = rf_model.predict(future_df[['num', 'year', 'month', 'day']])
# 可视化呈现2025年预测结果（预测收视份额随集数变化趋势）
plt.plot(future_df['num'], future_predictions)
plt.xlabel('剧集')
plt.ylabel('收视份额(%)')  # 修改ylabel为收视份额(%)
plt.title('2025年类似《人民的名义》电视剧收视份额预测')
plt.savefig("2025年类似《人民的名义》电视剧收视份额预测")
plt.show()