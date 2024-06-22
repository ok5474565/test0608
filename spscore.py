import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

def cov_sort_key(row_series, problem_scores_mean):
    # 确保 row_series 是一维数组且与 problem_scores_mean 长度相同
    if len(row_series) != len(problem_scores_mean):
        raise ValueError("The length of row_series and problem_scores_mean must be the same.")
    
    # 计算协方差
    return np.cov(row_series, problem_scores_mean)[0, 1]

def main():
    st.title('S-P Chart and Analysis Tool')

    # 允许用户上传文件
    uploaded_file = st.file_uploader("Please upload your score statistics table (.xlsx)")
    if uploaded_file is not None:
        # 读取Excel文件
        data = pd.read_excel(uploaded_file)

        # 学生姓名和题目号码
        students = data.columns[1:]  # 第一列除了标题外都是学生姓名
        problems = data.index[1:]   # 第一行除了标题外都是题目号码

        # 构建DataFrame，排除标题"对象"
        scores = data.iloc[1:, 1:].astype(int)

        # 计算总分
        student_totals = scores.sum(axis=1)
        problem_totals = scores.sum(axis=0)

        # 将学生总分转换为DataFrame，并添加列名“总分”
        student_totals_df = pd.DataFrame({'总分': student_totals})

        # 计算协方差排序的键值
        student_covs = scores.apply(lambda row: cov_sort_key(row, problem_totals.values), axis=1)
        # 将协方差值添加到学生总分DataFrame中
        student_totals_df['cov'] = student_covs

        # 根据总分和协方差排序学生
        sorted_students_index = student_totals_df.sort_values(['总分', 'cov'], ascending=[False, False]).index

        # 根据问题总分排序问题
        sorted_problems_index = problem_totals.sort_values(ascending=False).index

        # 创建排序后的S-P表格
        sorted_sp_df = scores.loc[sorted_students_index, sorted_problems_index]

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
