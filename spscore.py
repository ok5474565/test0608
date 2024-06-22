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

        # 确保DataFrame的索引是学生姓名，列是题目
        # 假设第一行是题目，第一列是学生姓名
        col_names = data.iloc[0]  # 取第一行作为列名
        row_names = data.columns  # 取第一列作为行名
        data = data.set_index(row_names).transpose()  # 转置数据，使索引为学生姓名

        # 计算每个学生的总分
        student_totals = data.sum(axis=1)

        # 计算每个问题的总分
        problem_totals = data.sum(axis=0)

        # 根据总分排序学生索引和问题索引
        sorted_students_index = student_totals.sort_values(ascending=False).index
        sorted_problems_index = problem_totals.sort_values(ascending=False).index

        # 创建排序后的DataFrame
        sorted_data = data.loc[sorted_students_index, sorted_problems_index]

        # 显示排序后的DataFrame
        st.write("S-P 表格:")
        st.dataframe(sorted_data)

# 运行主函数
if __name__ == '__main__':
    main()
