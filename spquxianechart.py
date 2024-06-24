import streamlit as st
import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.globals import ThemeType

# 上传xlsx文件
uploaded_file = st.file_uploader("上传得分统计表格 (xlsx)", type="xlsx")

if uploaded_file is not None:
    # 读取xlsx文件
    df = pd.read_excel(uploaded_file, index_col=0)
    
    # 去除第一行和第一列的无关内容
    df = df.iloc[1:, 1:]
    
    # 将值转换为数值类型
    df = df.apply(pd.to_numeric)

    # 统计每一行和每一列的得分计数
    row_sums = df.sum(axis=1)
    col_sums = df.sum(axis=0)

    # 在DataFrame最后一行和最后一列添加统计结果
    df.loc['总计'] = col_sums
    df['总计'] = row_sums
    st.write("统计后的表格：")
    st.dataframe(df)

    # 计算S曲线（每个学生的正确率）和P曲线（每个题目的正确率）
    s_curve = df.iloc[:-1, :-1].mean(axis=1).sort_values(ascending=False)
    p_curve = df.iloc[:-1, :-1].mean(axis=0).sort_values(ascending=True)

    # 使用ECharts绘制S-P曲线图
    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(list(range(1, len(s_curve) + 1)))
        .add_yaxis("S曲线 - 学生表现", s_curve.values.tolist(), is_smooth=True, linestyle_opts=opts.LineStyleOpts(type_="dashed"))
        .add_yaxis("P曲线 - 题目难度", p_curve.values.tolist(), is_smooth=True)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="S-P 曲线图"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            xaxis_opts=opts.AxisOpts(type_="category", name="索引"),
            yaxis_opts=opts.AxisOpts(type_="value", name="正确率"),
            legend_opts=opts.LegendOpts(pos_top="10%")
        )
    )

    st.write("S-P 曲线图：")
    st_pyecharts(line)

