import streamlit as st
import pandas as pd
import numpy as np

# Streamlit界面设置
def main():
    st.title('学生得分统计与S-P表格生成')

    # 用户上传文件
    uploaded_file = st.file_uploader("请上传您的 Excel 文件 (.xlsx)", type=["xlsx"])
    if uploaded_file is not None:
        # 读取文件
        data = pd.read_excel(uploaded_file)

        # 移除包含"对象"的单元格，假设"对象"在第一行第一列
        if '对象' in data.iloc[0, 0]:
            data = data.iloc[1:, 1:]  # 移除标题行和列

        # 计算每个学生的总分
        student_totals = data.sum(axis=1)

        # 计算每个问题的总分
        problem_totals = data.sum(axis=0)

        # 根据学生总分和问题总分排序
        sorted_students = student_totals.sort_values(ascending=False)
        sorted_problems = problem_totals.sort_values(ascending=False)

        # 创建一个列表来保存带有协方差分数的元组 (学生索引, 协方差值)
        cov_scores = []

        # 计算协方差并根据总分相同的学生进行排序
        for student_index in sorted_students.index:
            student_scores = data.loc[student_index]
            cov_value = np.cov(student_scores, problem_totals)[0][1]  # 取协方差值
            cov_scores.append((student_index, cov_value))

        # 根据协方差值排序学生，如果总分相同，则按协方差值排序
        cov_scores.sort(key=lambda x: (-x[0] in sorted_students.index) * abs(x[1]), reverse=True)

        # 提取排序后的学生索引
        sorted_student_indices = [index for index, _ in cov_scores if index in sorted_students.index]

        # 根据问题总分相同的问题进行协方差排序
        cov_problem_scores = []
        for problem_index in sorted_problems.index:
            problem_scores = data.loc[:, problem_index]
            cov_value = np.cov(problem_scores, student_totals)[0][1]  # 取协方差值
            cov_problem_scores.append((problem_index, cov_value))

        # 根据协方差值排序问题
        sorted_problem_indices = [index for _, index in sorted(cov_problem_scores, key=lambda x: (-sorted_problems.index.index(x[1])) * abs(x[0]), reverse=True)]

        # 根据排序后的学生和问题索引重新排列DataFrame
        sorted_data = data.loc[sorted_student_indices, sorted_problem_indices]

        # 显示排序后的DataFrame
        st.write("S-P 表格:")
        st.dataframe(sorted_data)

# 运行主函数
if __name__ == '__main__':
    main()
