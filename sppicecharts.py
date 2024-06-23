import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

def main():
    st.title('读取S-P表格生成S-P曲线图echarts')
    # 上传文件
    uploaded_file = st.file_uploader("上传 S-P 表格文件 (xlsx 或 csv)", type=["xlsx"])

    if uploaded_file is not None:
        # 读取文件
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)

        # 提取学生姓名和题目名称（跳过第一行和第一列）
        student_names = df.iloc[1:, 0].values
        question_titles = df.columns[1:].values

        # 提取答题数据
        data = df.iloc[1:, 1:].astype(int).values

        # 创建 DataFrame 并转置数据
        df_transposed = pd.DataFrame(data, index=student_names, columns=question_titles).transpose()

        # 计算学生总分（S曲线）
        s_curve = df_transposed.mean(axis=0).sort_values(ascending=False)

        # 计算每个问题的正答次数（P曲线）
        p_curve = df_transposed.mean(axis=1).sort_values(ascending=True)

        # 准备 S 曲线数据
        s_curve_data = [{'value': val, 'name': idx} for idx, val in enumerate(s_curve.values)]
        s_curve_normalized_index = list(range(len(s_curve)))

        # 准备 P 曲线数据
        p_curve_data = [{'value': val, 'name': idx} for idx, val in enumerate(p_curve.values)]
        p_curve_normalized_index = list(range(len(p_curve)))

        # 配置 S 曲线和 P 曲线的选项
        options = {
            "title": {
                "text": "综合 S 和 P 曲线"
            },
            "tooltip": {
                "trigger": "axis"
            },
            "legend": {
                "data": ["S 曲线 - 学生表现", "P 曲线 - 题目难度"]
            },
            "xAxis": {
                "type": "category",
                "data": s_curve_normalized_index
            },
            "yAxis": {
                "type": "value"
            },
            "series": [
                {
                    "name": "S 曲线 - 学生表现",
                    "type": "line",
                    "data": s_curve_data,
                    "lineStyle": {
                        "type": "dashed"
                    }
                },
                {
                    "name": "P 曲线 - 题目难度",
                    "type": "line",
                    "data": p_curve_data
                }
            ]
        }

        # 展示图表
        st_echarts(options=options)

if __name__ == "__main__":
    main()
