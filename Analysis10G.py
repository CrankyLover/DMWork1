import pyarrow.parquet as pq
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import time


if __name__ == "__main__" :

    country_frequency_dict = {}
    email_frequency_dict = {}
    invaild_email_number = 0
    invalid_age_number = 0
    all_number = 0
    country_email_dict = {}

    item_category_dict = {}
    category_freq = {}

    country_income_dict = {}

    with open("category_freq.json", encoding="utf-8") as f:
        category_freq = json.load(f)
    with open("email_frequency_dict.json", encoding="utf-8") as f:
        email_frequency_dict = json.load(f)
    with open("country_email_dict.json", encoding="utf-8") as f:
        country_email_dict = json.load(f)
    with open("item_category_dict.json", encoding="utf-8") as f:
        item_category_dict = json.load(f)
    with open("country_frequency_dict.json", encoding="utf-8") as f:
        country_frequency_dict = json.load(f)
    with open("country_income_dict.json", encoding="utf-8") as f:
        country_income_dict = json.load(f)

    lines = []
    with open("number.txt") as f:
        lines = f.readlines()
    
    all_number = int(lines[0])
    invaild_email_number = int(lines[1])
    invalid_age_number = int(lines[2])

    print(category_freq)
    画图，country_frequency_dict柱状图
    countries = list(country_frequency_dict.keys())
    frequencies = list(country_frequency_dict.values())
    plt.rcParams["font.sans-serif"] = "SimHei"
    plt.rcParams["axes.unicode_minus"] = False

    # 创建绘图画布
    plt.figure(figsize=(12, 6), dpi=100)  # 设置图形大小和分辨率

    # 绘制柱状图
    bars = plt.bar(
        x=countries,
        height=frequencies,
        color=['#4C72B0', '#55A868', '#C44E52', '#8172B2', '#CCB974', '#64B5CD'],  # 自定义颜色序列
        edgecolor='black',    # 边框颜色
        linewidth=1.2,        # 边框粗细
        alpha=0.9             # 透明度
    )

    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        plt.text(
            x=bar.get_x() + bar.get_width()/2,  # 文本X位置居中
            y=height + 0.02*max(frequencies),   # 文本Y位置微调
            s=f"{height}",                      # 显示数值
            ha='center',                        # 水平居中
            va='bottom',                        # 垂直对齐
            fontsize=10
        )

    # 设置图表元素
    plt.title("国家频率分布统计", fontsize=16, pad=20)
    plt.xlabel("国家名称", fontsize=12, labelpad=10)
    plt.ylabel("用户数量", fontsize=12, labelpad=10)
    plt.xticks(
        rotation=45,          # X轴标签旋转45度
        ha='right',           # 标签水平对齐方式
        fontsize=10
    )
    plt.grid(
        axis='y',             # 只显示横向网格线
        alpha=0.4,            # 网格透明度
        linestyle='--'        # 虚线样式
    )

    plt.savefig('country_frequency.png')

    emails = list(email_frequency_dict.keys())
    counts = list(email_frequency_dict.values())

    # 创建图形
    plt.figure(figsize=(10, 6))

    # 绘制柱状图，使用不同颜色
    colors = ['skyblue', 'lightgreen', 'orange', 'pink', 'lightblue', 'gray']
    plt.bar(emails, counts, color=colors)

    # 设置x轴标签旋转45度，右对齐
    plt.xticks(rotation=45, ha='right')

    # 设置坐标轴标签和标题
    plt.xlabel('Email Service Provider')
    plt.ylabel('Number of Accounts (millions)')
    plt.title('Distribution of Email Services')

    # 格式化y轴为百万单位
    def format_millions(x, pos):
        return f'{x / 1e6:.1f}M'
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_millions))

    # 调整布局并显示
    plt.tight_layout()
    plt.savefig('email_frequency.png')


    
    countries = list(country_email_dict.keys())
    services = list(country_email_dict[countries[0]].keys())  # 假设所有国家服务类型一致

    # 转换数据结构：{服务: [各国数值列表]}
    service_values = {service: [country_email_dict[country][service] for country in countries] for service in services}

    # 创建图形
    fig, ax = plt.subplots(figsize=(18, 8))

    # 配置柱状图参数
    x = np.arange(len(countries))          # 国家位置坐标
    total_width = 0.8                      # 每组柱子的总宽度
    service_width = total_width / len(services)  # 单个服务柱宽
    colors = plt.cm.tab10.colors[:len(services)]  # 使用标准颜色

    # 绘制每个服务的柱子
    for i, (service, values) in enumerate(service_values.items()):
        offset = (i - len(services)/2) * service_width + service_width/2
        ax.bar(x + offset,
            values,
            width=service_width,
            label=service,
            color=colors[i])

    # 配置坐标轴
    ax.set_xticks(x)
    ax.set_xticklabels(countries, rotation=45, ha='right')
    ax.set_ylabel('Frequency (millions)')

    # 添加百万单位格式化
    def million_formatter(x, pos):
        return f'{x/1e6:.2f}M'
    ax.yaxis.set_major_formatter(FuncFormatter(million_formatter))

    # 添加辅助元素
    ax.set_title('emails in each country', pad=20)
    ax.legend(title='emails', bbox_to_anchor=(1.05, 1), loc='upper left')

    # 调整布局
    plt.tight_layout()
    plt.savefig("country_email_freqency.png")



    将所有值除以 all_number
    scaled_income_data = {country: income / all_number for country, income in country_income_dict.items()}

    # 生成不同的颜色
    colors = plt.cm.get_cmap("tab10", len(scaled_income_data))

    # 绘制柱状图
    plt.figure(figsize=(10, 6))
    bars = plt.bar(scaled_income_data.keys(), scaled_income_data.values(), color=colors(range(len(scaled_income_data))))

    # 设置标题和标签
    plt.title("Countries Income Scaled by all_number", fontsize=14)
    plt.xlabel("Country", fontsize=12)
    plt.ylabel("Scaled Income (Income / all_number)", fontsize=12)

    # 显示图表
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("country_income.png")

    # 饼图的绘制
    plt.figure(figsize=(10, 8))
    plt.pie(category_freq.values(), labels=category_freq.keys(), autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title('freq')
    plt.axis('equal')  # 保证饼图是圆形的
    plt.savefig('category_frequency.png')

    new_category_dict = {"基础饮食类": 0,
                         "厨房类": 0,
                         "食品类": 0,
                         "衣物类": 0,
                         "电子产品类": 0,
                         "家庭产品类": 0,
                         "幼儿产品类": 0,
                         "户外类": 0}
    
    mapping_dict = {"水产":"基础饮食类", "蔬菜":"基础饮食类", "肉类":"基础饮食类", "蛋奶":"基础饮食类", "米面":"基础饮食类", "水果":"基础饮食类",
                    "调味品":"厨房类", "厨具":"厨房类",
                    "零食":"食品类", "饮料":"食品类",
                    "内衣":"衣物类", "上衣":"衣物类", "围巾":"衣物类", "裤子":"衣物类", "外套":"衣物类", "鞋子":"衣物类", "帽子":"衣物类", "裙子":"衣物类", "手套":"衣物类",
                    "智能手机":"电子产品类", "平板电脑":"电子产品类", "游戏机":"电子产品类", "笔记本电脑":"电子产品类", "办公用品":"电子产品类", "耳机":"电子产品类", "音响":"电子产品类", "智能手表":"电子产品类", "摄像机":"电子产品类", "车载电子":"电子产品类", "相机":"电子产品类", 
                    "家具":"家庭产品类", "床上用品":"家庭产品类", "卫浴用品":"家庭产品类", "汽车装饰":"家庭产品类",
                    "益智玩具":"幼儿产品类", "模型":"幼儿产品类", "婴儿用品":"幼儿产品类", "儿童课外读物":"幼儿产品类", "玩具":"幼儿产品类", "文具":"幼儿产品类",
                    "健身器材":"户外类", "户外装备":"户外类"
                    }
    
    for item in item_category_dict:
        for cate in item_category_dict[item]:
            freq = item_category_dict[item][cate]
            new_category_dict[mapping_dict[cate]] += freq

    new_cate = list(new_category_dict.keys())
    new_cate_value = list(new_category_dict.values())

    # 创建图形
    plt.figure(figsize=(10, 6))

    # 绘制柱状图，使用不同颜色
    colors = ['skyblue', 'lightgreen', 'orange', 'pink', 'lightblue', 'gray']
    plt.bar(new_cate, new_cate_value, color=colors)

    # 设置x轴标签旋转45度，右对齐
    plt.xticks(rotation=45, ha='right')

    # 设置坐标轴标签和标题
    plt.xlabel('Item Categories')
    plt.ylabel('Number of user purchase')
    plt.title('Distribution of User Purchase')

    # 格式化y轴为百万单位
    def format_millions(x, pos):
        return f'{x / 1e6:.1f}M'
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_millions))

    # 调整布局并显示
    plt.tight_layout()
    plt.savefig('user_behavior.png')

    plt.figure(figsize=(10, 8))
    plt.pie(new_category_dict.values(), labels=new_category_dict.keys(), autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title('freq')
    plt.axis('equal')  # 保证饼图是圆形的
    plt.savefig('user_behavior_b.png')

    print(len(item_category_dict))
                         
