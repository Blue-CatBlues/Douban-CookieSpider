import pandas as pd
import numpy as np
import matplotlib
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import json
from matplotlib.animation import FuncAnimation
matplotlib.use('TkAgg')

# 设置全局字体为雅黑，便于图表中中文正常显示
plt.rcParams['font.family'] = ['Microsoft YaHei']
# 设置全局轴标签字号大小，使图表展示更美观、清晰
plt.rcParams['axes.labelsize'] = 14


def load_data(file_path):
    """
    从指定的JSON文件中加载数据，并转换为Pandas的DataFrame格式

    :param file_path: JSON文件的路径
    :return: DataFrame类型的数据
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data)


def preprocess_data(df):
    """
    对输入的DataFrame进行数据预处理，包括日期特征提取和集数的类型转换

    :param df: 原始数据的DataFrame
    :return: 处理后的特征数据（X）以及目标变量（y_city_tv、y_china_tv）
    """
    # 将日期列转换为可用于模型训练的数值特征（提取年、月、日）
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day

    # 选择用于模型训练的特征列
    features = ['num', 'year', 'month', 'day']
    X = df[features]
    # 将集数列转换为整数类型，确保数据类型符合模型要求
    # 使用 .loc 明确指定要修改的是原 DataFrame 的一部分
    X.loc[:, 'num'] = X['num'].astype(int)

    # 提取目标变量，即CSM52城市网收视率%和CSM全国网收视率%，并调整数据形状
    y_city_tv = df['city_tv_per'].astype(float).values.ravel()  # 修改为 ravel()
    y_china_tv = df['china_tv_per'].astype(float).values.ravel()  # 修改为 ravel()

    return X, y_city_tv, y_china_tv


def generate_future_data(num_episodes):
    """
    模拟生成指定集数的未来数据，用于后续预测

    :param num_episodes: 要模拟的数据的集数
    :return: 包含模拟数据的DataFrame（X_predict）
    """
    # 生成指定日期范围的数据，这里模拟2025年每天的数据
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


def train_models(X, y_city_tv, y_china_tv):
    """
    初始化并训练随机森林回归模型，分别用于预测CSM52城市网和CSM全国网的收视率

    :param X: 训练数据的特征部分
    :param y_city_tv: CSM52城市网收视率%的目标变量
    :param y_china_tv: CSM全国网收视率%的目标变量
    :return: 训练好的两个随机森林回归模型
    """
    # 初始化用于预测CSM52城市网收视率的随机森林回归模型，设置相关参数
    rf_model_city_tv = RandomForestRegressor(n_estimators=100, random_state=42)
    # 初始化用于预测CSM全国网收视率的随机森林回归模型，设置相关参数
    rf_model_china_tv = RandomForestRegressor(n_estimators=100, random_state=42)

    # 训练用于预测CSM52城市网收视率的模型
    rf_model_city_tv.fit(X, y_city_tv)
    # 训练用于预测CSM全国网收视率的模型
    rf_model_china_tv.fit(X, y_china_tv)

    return rf_model_city_tv, rf_model_china_tv


def predict_with_models(models, X_predict):
    """
    使用训练好的模型对模拟数据进行预测

    :param models: 包含两个训练好的随机森林回归模型的元组
    :param X_predict: 模拟数据的特征部分，用于预测
    :return: 两个模型分别对模拟数据预测的结果（y_pred_city_tv、y_pred_china_tv）
    """
    rf_model_city_tv, rf_model_china_tv = models
    # 利用训练好的模型预测CSM52城市网收视率
    y_pred_city_tv = rf_model_city_tv.predict(X_predict)
    # 利用训练好的模型预测CSM全国网收视率
    y_pred_china_tv = rf_model_china_tv.predict(X_predict)

    return y_pred_city_tv, y_pred_china_tv


def update(frame):
    """
    更新每一帧动画的绘制内容，绘制两条不同颜色的线并简化注释
    """
    ax.clear()
    ax.plot(np.arange(1, frame + 1), y_pred_city_tv_result[:frame], label='城市网', marker='o', color='blue')
    ax.plot(np.arange(1, frame + 1), y_pred_china_tv_result[:frame], label='全国网', marker='s', color='red')
    ax.set_xlabel('集数')
    ax.set_ylabel('收视率%')
    ax.set_title('2025年类似《人民的名义》电视剧CSM52两站收视率对比预测')
    ax.legend()
    ax.grid(True)


if __name__ == "__main__":
    # 数据文件路径，可根据实际情况调整
    data_file_path = 'new_TV_info.json'
    # 模拟预测的集数
    num_episodes_to_predict = 30

    # 加载数据
    data_df = load_data(data_file_path)
    # 数据预处理
    X_data, y_city_tv_data, y_china_tv_data = preprocess_data(data_df)
    # 生成模拟预测数据
    X_predict_data = generate_future_data(num_episodes_to_predict)
    # 训练模型
    trained_models = train_models(X_data, y_city_tv_data, y_china_tv_data)
    # 使用模型进行预测
    y_pred_city_tv_result, y_pred_china_tv_result = predict_with_models(trained_models, X_predict_data)

    fig, ax = plt.subplots(figsize=(12, 6))
    ani = FuncAnimation(fig, update, frames=num_episodes_to_predict, interval=200, repeat=False)
    plt.show()