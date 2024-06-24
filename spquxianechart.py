import pandas as pd
import streamlit as st
import pyecharts
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode

@st.cache
def load_data(uploaded_file):
    df = pd.read_excel(uploaded_file, index_col=0)
    # 忽略第一列姓名和第一行题目
    df = df.iloc[1:, 1:]
    return df

def calculate_scores(df):
    # 计算每行的总分
    df['Total Score by Student'] = df.sum(axis=1)
    # 计算每列的总分
    df.loc['Total Score by Problem'] = df.sum(axis=0)
    return df

def generate_sp_chart(df):
    # 创建S曲线和P曲线数据
    s_curve = df['Total Score by Student'].sort_values(ascending=False)
    p_curve = df.loc['Total Score by Problem'].sort_values(ascending=True)

    # 创建图表
    line_chart = Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    line_chart.add_xaxis(list(s_curve.index))
    line_chart.add_yaxis("Student Scores", s_curve.values.tolist(), is_smooth=True, linestyle_opts=opts.LineStyleOpts(width=2, type_="dashed"))
    line_chart.add_yaxis("Problem Scores", p_curve.values.tolist(), is_smooth=True)
    line_chart.set_global_opts(title_opts=opts.TitleOpts(title="S-P Curve Analysis"),
                               tooltip_opts=opts.TooltipOpts(is_show=True, formatter=JsCode(
                                   "function (params) {return params.name + ': ' + params.value;}")),
                               yaxis_opts=opts.AxisOpts(type_="value", min_=0, max_=df.shape[0]),
                               xaxis_opts=opts.AxisOpts(type_="category"))
    return line_chart

def main():
    st.title("S-P Curve Analysis Tool")
    uploaded_file = st.file_uploader("Please upload your score table (xlsx format):", type=["xlsx"])
    if uploaded_file:
        data = load_data(uploaded_file)
        calculated_data = calculate_scores(data)
        chart = generate_sp_chart(calculated_data)
        st.write(calculated_data.iloc[:-1, :-1])  # 显示处理后的数据，不包括最后一行和最后一列
        st.pyecharts_chart(chart)

if __name__ == "__main__":
    main()
