import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

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
        s_curve = s_curve.sort_values(ascending=False)
        p_curve = p_curve.sort_values(ascending=True)

        # 准备绘图数据
        s_curve_data = [{'x': str(i), 'y': val} for i, val in enumerate(s_curve.values)]
        p_curve_data = [{'x': str(i), 'y': val} for i, val in enumerate(p_curve.values)]
        
        options = {
            "title": {
                "text": 'S-P 曲线图'
            },
            "tooltip": {
                "trigger": 'axis'
            },
            "legend": {
                "data": ['S 曲线 - 学生表现', 'P 曲线 - 问题难度']
            },
            "xAxis": {
                "type": 'category',
                "boundaryGap": False,
                "data": [str(i) for i in range(len(s_curve))]
            },
            "yAxis": {
                "type": 'value'
            },
            "series": [
                {
                    "name": 'S 曲线 - 学生表现',
                    "type": 'line',
                    "data": s_curve_data,
                    "lineStyle": {
                        "type": 'dashed',
                        "color": 'red'
                    }
                },
                {
                    "name": 'P 曲线 - 问题难度',
                    "type": 'line',
                    "data": p_curve_data,
                    "lineStyle": {
                        "color": 'blue'
                    }
                }
            ]
        }
        
        # 使用 Streamlit Echarts 绘制图表
        st_echarts(options=options)

if __name__ == "__main__":
    main()
