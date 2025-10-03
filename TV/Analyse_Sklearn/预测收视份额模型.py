import pandas as pd
import numpy as np
import matplotlib
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import json
from matplotlib.animation import FuncAnimation
matplotlib.use('TkAgg')

# 设置全局字体为雅黑，增强图表中文显示效果
plt.rcParams['font.family'] = ['Microsoft YaHei']
# 设置全局轴标签字号大小，使图表标签显示更清晰
plt.rcParams['axes.labelsize'] = 14


def load_data(file_path):
    """
    从指定的JSON文件中加载数据，并转换为DataFrame格式

    :param file_path: JSON文件的路径
    :return: 包含数据的DataFrame对象
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data)


def preprocess_data(df):
    """
    对输入的DataFrame进行数据预处理，包括日期特征提取和集数编码转换

    :param df: 原始数据的DataFrame
    :return: 处理好特征的DataFrame（X）以及目标变量（y_city_tv_per, y_china_tv_per）
    """
    # 将日期列转换为可用于模型训练的数值特征（提取年、月、日）
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day

    # 选择用于模型训练的特征列
    features = ['num', 'year', 'month', 'day']
    X = df[features]

    # 使用.loc明确指定要修改的是原DataFrame的一部分
    X.loc[:, 'num'] = X['num'].astype(int)

    # 提取目标变量，并转换为一维数组
    y_city_tv_per = df['city_tv_per'].astype(float).values.ravel()
    y_china_tv_per = df['china_tv_per'].astype(float).values.ravel()

    return X, y_city_tv_per, y_china_tv_per


def simulate_future_data(num_episodes):
    """
    模拟生成未来指定集数的数据，用于预测

    :param num_episodes: 需要模拟的数据的集数
    :return: 模拟数据构成的DataFrame（X_predict）
    """
    # 生成日期范围，模拟2025年每天的数据
    predict_dates = pd.date_range(start='2025-01-01', periods=num_episodes, freq='D')
    predict_data = []
    for i in range(1, num_episodes + 1):
        date = predict_dates[i - 1]
        row = {'num': i, 'year': date.year, 'month': date.month, 'day': date.day}
        predict_data.append(row)

    predict_df = pd.DataFrame(predict_data)
    features = ['num', 'year', 'month', 'day']
    X_predict = predict_df[features]
    X_predict['num'] = X_predict['num'].astype(int)
    return X_predict


def train_and_predict(X, y_city_tv_per, y_china_tv_per, X_predict):
    """
    使用随机森林回归模型进行训练，并对模拟数据进行预测

    :param X: 训练数据的特征
    :param y_city_tv_per: CSM52城市网收视份额%的目标变量
    :param y_china_tv_per: CSM全国网收视份额%的目标变量
    :param X_predict: 模拟数据的特征，用于预测
    :return: 两个模型分别对模拟数据预测的结果（y_pred_city_tv_per, y_pred_china_tv_per）
    """
    # 初始化随机森林回归模型，设置估计器数量及随机种子
    rf_model_city_tv_per = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model_china_tv_per = RandomForestRegressor(n_estimators=100, random_state=42)

    # 训练模型
    rf_model_city_tv_per.fit(X, y_city_tv_per)
    rf_model_china_tv_per.fit(X, y_china_tv_per)

    # 预测CSM52城市网收视份额%
    y_pred_city_tv_per = rf_model_city_tv_per.predict(X_predict)
    # 预测CSM全国网收视份额%
    y_pred_china_tv_per = rf_model_china_tv_per.predict(X_predict)

    return y_pred_city_tv_per, y_pred_china_tv_per


def update(frame):
    """
    更新每一帧动画的绘制内容，使用两种颜色绘制两条线并只保留两个线注释
    """
    ax.clear()  # 清除之前绘制的内容
    ax.plot(np.arange(1, frame + 1), y_pred_city_tv_per[:frame], label='城市网', marker='o', color='blue')
    ax.plot(np.arange(1, frame + 1), y_pred_china_tv_per[:frame], label='全国网', marker='s', color='red')
    ax.set_xlabel('集数')
    ax.set_ylabel('收视份额%')
    ax.set_title('2025年类似《人民的名义》电视剧CSM52两站收视份额对比预测')
    ax.legend()
    ax.grid(True)


if __name__ == "__main__":
    # JSON数据文件路径，可根据实际情况修改
    data_file_path = 'new_TV_info.json'
    # 模拟预测的集数
    num_episodes_to_predict = 30

    # 加载数据
    df = load_data(data_file_path)

    # 数据预处理
    X, y_city_tv_per, y_china_tv_per = preprocess_data(df)
    # 模拟未来数据
    X_predict = simulate_future_data(num_episodes_to_predict)
    # 训练模型并预测
    y_pred_city_tv_per, y_pred_china_tv_per = train_and_predict(X, y_city_tv_per, y_china_tv_per, X_predict)

    fig, ax = plt.subplots(figsize=(12, 6))
    ani = FuncAnimation(fig, update, frames=num_episodes_to_predict, interval=200, repeat=False)
    plt.show()