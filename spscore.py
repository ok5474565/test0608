import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

def main():
    st.title('S-P Chart and Analysis Tool')

    # 允许用户上传文件
    uploaded_file = st.file_uploader("Please upload your score statistics table (.xlsx)")

    if uploaded_file is not None:
        # 读取Excel文件
        data = pd.read_excel(uploaded_file)

        # 学生姓名是第一列的值（除了标题）
        students = data.iloc[1:, 0].values  # 从第二行开始取第一列的所有值

        # 题目名称是第一行的值（除了标题）
        problems = data.iloc[0, 1:].values  # 取第一行的第二列到最后一列的值

        # 构建DataFrame，排除标题行和列
        scores = data.iloc[1:, 1:].astype(int)  # 从第二行第二列开始选取所有数据，并转换为整数类型

        # 创建DataFrame，行列索引分别为学生和题目
        sp_df = pd.DataFrame(scores, index=students, columns=problems)

        # 计算每个学生的总分和每个问题的总分
        student_totals = sp_df.sum(axis=1)
        problem_totals = sp_df.sum(axis=0)

        # 根据总分排序学生
        sorted_students = student_totals.sort_values(ascending=False)

        # 根据总分排序问题
        sorted_problems = problem_totals.sort_values(ascending=False)

        # 创建排序后的S-P表格
        sorted_sp_df = sp_df.loc[sorted_students.index, sorted_problems.index]

        # 显示S-P表格
        st.write("S-P Table:")
        st.table(sorted_sp_df)

        # 绘制S-P曲线
        s_curve = sorted_sp_df.mean(axis=1)
        p_curve = sorted_sp_df.mean(axis=0)

        plt.figure(figsize=(10, 6))
        plt.plot(s_curve, marker='o', color='blue', label='S Curve - Student Performance')
        plt.plot(p_curve, marker='o', color='red', label='P Curve - Problem Difficulty')
        plt.title('S-P Curves')
        plt.xlabel('Index')
        plt.ylabel('Score')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        # 转换图表为图片
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        # 显示图表
        st.image(buf, caption='S-P Curves', use_column_width=True)

        # 计算差异系数和注意系数
        average_scores = sp_df.mean()
        std_dev_scores = sp_df.std()
        cv = std_dev_scores / average_scores
        attention_coefficient = 1 - average_scores

        # 显示统计数据
        summary_df = pd.DataFrame({
            'Average Score': average_scores,
            'Standard Deviation': std_dev_scores,
            'Coefficient of Variation (CV)': cv,
            'Attention Coefficient': attention_coefficient
        }, index=problems)
        st.write("Summary Statistics:")
        st.table(summary_df)

if __name__ == "__main__":
    main()
