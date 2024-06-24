import streamlit as st
import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts
import numpy as np

def load_data(uploaded_file):
    # 读取数据，跳过第一行第一列
    data = pd.read_excel(uploaded_file, index_col=0, header=0)
    # 计算每一行和每一列的总得分
    data['总得分'] = data.sum(axis=1)
    data.loc['总得分'] = data.sum(axis=0)
    return data

def generate_sp_chart(data):
    # 计算每位用户的正确率
    scores = data.loc[:, data.columns != '总得分']
    total_questions = len(scores.columns)
    scores['正确率'] = scores.sum(axis=1) / total_questions

    # 准备数据
    sorted_scores = scores['正确率'].sort_values()
    count = len(sorted_scores)
    x_data = [(i+1)/count for i in range(count)]
    y_data = sorted_scores.tolist()

    # 创建图表
    chart = Line()
    chart.add_xaxis(x_data)
    chart.add_yaxis("正确率", y_data)
    chart.set_global_opts(
        title_opts=opts.TitleOpts(title="S-P 曲线图"),
        xaxis_opts=opts.AxisOpts(name="百分位"),
        yaxis_opts=opts.AxisOpts(name="正确率"),
    )
    return chart

def main():
    st.title("S-P 曲线图生成器")

    uploaded_file = st.file_uploader("请选择一个Excel文件", type="xlsx")
    if uploaded_file:
        data = load_data(uploaded_file)
        st.write("数据预览（包含总得分）：", data)

        # 绘制S-P曲线图
        chart = generate_sp_chart(data)
        st_pyecharts(chart)

if __name__ == "__main__":
    main()
