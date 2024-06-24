import streamlit as st
import pandas as pd
from st_echarts import st_echarts

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

        # 准备 ECharts 图表的数据
        s_curve_data = [(i, value) for i, value in enumerate(s_curve_sorted.values)]
        p_curve_data = [(i, value) for i, value in enumerate(p_curve_sorted.values)]

        # 创建 ECharts 图表
        chart = (
            st_echarts()
            .set_option(
                "title", "S-P 曲线图"
            )
            .set_global_options(
                xaxis_type="category",
                yaxis_type="value",
                toolbox_feature="restore,save",
            )
            .add(
                "line",
                "S 曲线 - 学生表现",
                s_curve_data,
                is_more_utils=True,
            )
            .add(
                "line",
                "P 曲线 - 问题难度",
                p_curve_data,
                is_more_utils=True,
            )
        )

        # 显示图表
        st.write(chart)

if __name__ == "__main__":
    main()
