import streamlit as st
import pandas as pd
from st_echarts import ECharts, StGrid, StLine

def main():
    st.title('S-P 曲线图生成器')

    # 上传文件
    uploaded_file = st.file_uploader("上传得分统计表格 (.xlsx 文件)", type=["xlsx"])

    if uploaded_file is not None:
        # 读取 Excel 文件
        df = pd.read_excel(uploaded_file)

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

        # 准备 ECharts 图表的数据
        s_curve_data = s_curve_sorted.tolist()
        p_curve_data = p_curve_sorted.tolist()

        # 创建 ECharts 图表
        line = (
            ECharts()
            .set_option(
                x_axis_min=0,
                x_axis_max=len(s_curve_sorted),
                y_axis_scale=True,
                title="S-P 曲线图",
                legend_data=["S 曲线 - 学生表现", "P 曲线 - 问题难度"]
            )
            .add(
                "line",  # 图表类型
                ["S 曲线 - 学生表现", s_curve_data],  # 系列名称和数据
                is_symbol_show=True,
                is_smooth=True,
                is_xaxis_show=True,
                is_yaxis_show=True,
                is_legend_show=True
            )
            .add(
                "line",  # 图表类型
                ["P 曲线 - 问题难度", p_curve_data],  # 系列名称和数据
                is_symbol_show=True,
                is_smooth=True,
                is_xaxis_show=True,
                is_yaxis_show=True,
                is_legend_show=True
            )
        )

        # 显示图表
        st.write(line)

if __name__ == "__main__":
    main()
