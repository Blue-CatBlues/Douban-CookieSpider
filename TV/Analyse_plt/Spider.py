import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib.font_manager as fm
import json
from datetime import datetime

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号

# 定义文件路径
base_path = r'D:\AAAPycharmProjects\TV'
actors_info_file = os.path.join(base_path, 'actors_info.json')
tv_info_file = os.path.join(base_path, 'TV_info.json')

# 打印当前工作目录
print("Current working directory:", os.getcwd())

# 检查文件是否存在
def check_file_exists(file_path):
    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} does not exist.")
        return False
    return True

# 读取JSON文件并转换为DataFrame
def load_json_to_df(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return pd.DataFrame(data)

if check_file_exists(actors_info_file):
    df_actors = load_json_to_df(actors_info_file)
if check_file_exists(tv_info_file):
    df_tv = load_json_to_df(tv_info_file)

# 数据预处理

# 确保TV数据中的数值字段是浮点数
def preprocess_tv_data(df):
    df['city_tv'] = pd.to_numeric(df['city_tv'], errors='coerce')
    df['city_tv_per'] = pd.to_numeric(df['city_tv_per'], errors='coerce')
    df['china_tv'] = pd.to_numeric(df['china_tv'], errors='coerce')
    df['china_tv_per'] = pd.to_numeric(df['china_tv_per'], errors='coerce')

    # Convert the 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

if 'df_tv' in locals() and not df_tv.empty:
    df_tv = preprocess_tv_data(df_tv)

# 计算演员年龄
def calculate_age(birth_day_str):
    if pd.isna(birth_day_str):
        return None
    try:
        birth_year = int(birth_day_str.split('年')[0])
        current_year = datetime.now().year
        return current_year - birth_year
    except (ValueError, IndexError):
        print(f"Warning: Invalid birth day format: {birth_day_str}")
        return None

if 'df_actors' in locals() and not df_actors.empty:
    df_actors['age'] = df_actors['birth_day'].apply(calculate_age)

# 分析演员年龄分布
def plot_actor_age_distribution(df):
    # 排除年龄为None的行
    valid_ages = df['age'].dropna()
    plt.figure(figsize=(10, 6))
    sns.histplot(valid_ages, bins=20, kde=True, color='skyblue')
    plt.title('演员年龄分布直方图')
    plt.xlabel('年 龄')
    plt.ylabel('人 数')
    plt.grid(True)
    plt.show()

# 分析演员生肖
def plot_actor_zodiac(df):
    zodiacs = {
        0: '猴', 1: '鸡', 2: '狗', 3: '猪', 4: '鼠', 5: '牛', 6: '虎',
        7: '兔', 8: '龙', 9: '蛇', 10: '马', 11: '羊'
    }

    def get_zodiac(birth_year):
        if pd.isna(birth_year):
            return None
        try:
            birth_year = int(birth_year.split('年')[0])
            return zodiacs[(birth_year - 1900) % 12]
        except (ValueError, IndexError):
            print(f"Warning: Invalid birth year format: {birth_year}")
            return None

    df['zodiac'] = df['birth_day'].apply(get_zodiac)
    zodiac_counts = df['zodiac'].value_counts()

    plt.figure(figsize=(10, 6))
    sns.barplot(x=zodiac_counts.index, y=zodiac_counts.values, hue=zodiac_counts.index, palette='viridis', legend=False)
    plt.title('演员生肖情况')
    plt.xlabel('生  肖')
    plt.ylabel('人  数')
    plt.grid(True)
    plt.show()

# 分析演员星座
def plot_actor_constellation(df):
    constellation_counts = df['constellation'].value_counts()

    plt.figure(figsize=(10, 6))
    plt.pie(constellation_counts, labels=constellation_counts.index, autopct='%1.1f%%',
            startangle=90, colors=sns.color_palette('pastel'))
    plt.title('演员星座分析')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

# 分析收视率情况
def plot_tv_ratings(df):
    if df.empty:
        print("No TV data to plot.")
        return

    plt.figure(figsize=(10, 6))
    sns.lineplot(x='date', y='city_tv', data=df, label='城市网', marker='o')
    sns.lineplot(x='date', y='china_tv', data=df, label='全国网', marker='x')
    plt.title('各时段电视收视率')
    plt.xlabel('日期')
    plt.ylabel('收视率')
    plt.legend()
    plt.grid(True)
    plt.show()

def analyze_tv_data(df):
    print("TV Data Summary:")
    print(df[['city_tv', 'china_tv']].describe())

    # 计算平均收视率
    avg_city_tv = df['city_tv'].mean()
    avg_china_tv = df['china_tv'].mean()
    print(f"Average City TV Rating: {avg_city_tv:.2f}")
    print(f"Average National TV Rating: {avg_china_tv:.2f}")

if 'df_actors' in locals() and not df_actors.empty:
    print("演员数据框的列名：")
    print(df_actors.columns.tolist())

# 调用函数绘制图表和进行统计分析
if 'df_actors' in locals() and not df_actors.empty:
    plot_actor_age_distribution(df_actors)
    plot_actor_zodiac(df_actors)
    plot_actor_constellation(df_actors)

if 'df_tv' in locals() and not df_tv.empty:
    plot_tv_ratings(df_tv)
    analyze_tv_data(df_tv)