import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

def cov_sort_key(df, row):
    # 获取问题得分向量
    problem_scores = df.sum(axis=1)
    # 计算协方差并返回，用于排序
    return np.cov(row, problem_scores)[0, 1]

def main():
    st.title('S-P Chart and Analysis Tool')

    # 允许用户上传文件
    uploaded_file = st.file_uploader("Please upload your score statistics table (.xlsx)")

    if uploaded_file is not None:
        # 读取Excel文件
        data = pd.read_excel(uploaded_file)

        # 移除标题行和列
        data = data.drop(data.columns[0], axis=1).drop(data.index[0])

        # 学生姓名和题目号码
        students = data.columns
        problems = data.index

        # 转换数据类型为整数
        scores = data.astype(int)

        # 计算总分
        student_totals = scores.sum(axis=1)
        problem_totals = scores.sum(axis=0)

        # 根据总分和协方差排序
        sorted_students_index = (student_totals.sort_values(ascending=False)
                                 .merge(pd.Series({idx: cov_sort_key(scores, scores.loc[idx, :]) for idx in scores.index}),
                                        left_index=True, right_index=True)
                                 .sort_values(by='cov', ascending=False)
                                 .index)
        sorted_problems_index = (problem_totals.sort_values(ascending=False)
                                 .merge(pd.Series({idx: cov_sort_key(scores.T, scores.T.loc[:, idx]) for idx in scores.columns}),
                                        left_index=True, right_index=True)
                                 .sort_values(by='cov', ascending=False)
                                 .index)

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
