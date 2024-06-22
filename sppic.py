import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.font_manager import FontProperties

# 假设 simhei.ttf 已经上传到你的 Streamlit 应用的根目录下
# 你需要根据实际上传的路径来设置 font_path
font_path = 'simhei.ttf'
chinese_font = FontProperties(fname=font_path, size=14)



def main():
    st.title('读取S-P表格生成S-P曲线图maplotlib')
    # 假设 simhei.ttf 已经上传到你的 Streamlit 应用的根目录下
    # 你需要根据实际上传的路径来设置 font_path
    font_path = 'simhei.ttf'
    chinese_font = FontProperties(fname=font_path, size=14)

    # 上传文件
    uploaded_file = st.file_uploader("上传 S-P 表格文件 (xlsx 或 csv)", type=["xlsx", "csv"])

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

        # 绘制 S 曲线和 P 曲线
        plt.figure(figsize=(12, 8))

        # 正规化索引
        s_curve_normalized_index = range(len(s_curve))
        p_curve_normalized_index = range(len(p_curve))

        # 绘制 S 曲线（虚线）
        plt.plot(s_curve_normalized_index, s_curve.values, 'r--', label='S 曲线 - 学生表现')

        # 绘制 P 曲线（实线）
        plt.plot(p_curve_normalized_index, p_curve.values, 'b-', label='P 曲线 - 题目难度')

        plt.title('综合 S 和 P 曲线', fontproperties=chinese_font)
        plt.xlabel('索引', fontproperties=chinese_font)
        plt.ylabel('百分比', fontproperties=chinese_font)
        plt.legend(prop=chinese_font)
        plt.tight_layout()

        # 展示图表
        st.pyplot(plt)

if __name__ == "__main__":
    main()
