import streamlit as st
import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts

def main():
    st.title('S-P 曲线图生成器')

    # 上传文件
    uploaded_file = st.file_uploader("上传得分统计表格 (.xlsx 文件)", type="xlsx")
    
    if uploaded_file:
        # 读取 Excel 文件
        df = pd.read_excel(uploaded_file, header=1, index_col=0)

        # 统计每行和每列的得分计数
        row_sums = df.sum(axis=1)
        col_sums = df.sum(axis=0)

        # 将统计结果添加到 DataFrame 中
        df['总分'] = row_sums
        df.loc['总计'] = col_sums

        st.write('更新后的数据表格:')
        st.dataframe(df)

        # 计算 S-Curve 和 P-Curve
        s_curve = row_sums / df.shape[1]
        p_curve = col_sums / df.shape[0]

        # 排序
        s_curve_sorted = s_curve.sort_values(ascending=False)
        p_curve_sorted = p_curve.sort_values(ascending=True)

        # 准备 S-P 曲线图的数据
        s_curve_data = [(index, value) for index, value in s_curve_sorted.items()]
        p_curve_data = [(index, value) for index, value in p_curve_sorted.items()]

        # 创建一个 Line 图对象
        line_chart = Line(init_opts=opts.InitOpts(width="1000px", height="600px"))

        # 添加 S 曲线和 P 曲线数据
        line_chart.add_xaxis([index for index, _ in s_curve_data])
        line_chart.add_yaxis("S 曲线 - 学生表现", [value for _, value in s_curve_data], is_smooth=True, linestyle_opts=opts.LineStyleOpts(width=2, type_='dashed'))
        line_chart.add_yaxis("P 曲线 - 问题难度", [value for _, value in p_curve_data], is_smooth=True, linestyle_opts=opts.LineStyleOpts(width=2))

        # 设置图表的全局选项
        line_chart.set_global_opts(
            title_opts=opts.TitleOpts(title="S-P 曲线图"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            legend_opts=opts.LegendOpts(pos_left="5%", pos_top="5%")
        )

        # 显示图表
        st.write(line_chart.render_embed())

if __name__ == "__main__":
    main()
