import streamlit as st
import pandas as pd
import numpy as np

def main():
    st.title('学生得分统计与S-P表格生成')

    # 用户上传文件
    uploaded_file = st.file_uploader("请上传您的 Excel 文件 (.xlsx)", type=["xlsx"])
    if uploaded_file is not None:
        # 读取文件，跳过第一行和第一列
        data = pd.read_excel(uploaded_file, header=1, skiprows=1)

        # 计算每个学生的总分
        student_totals = data.sum(axis=1)

        # 计算每个问题的总分
        problem_totals = data.sum(axis=0)

        # 根据总分排序学生索引和问题索引
        sorted_students_index = student_totals.sort_values(ascending=False).index
        sorted_problems_index = problem_totals.sort_values(ascending=False).index

        # 创建排序后的DataFrame
        sorted_data = data.loc[sorted_students_index, sorted_problems_index]

        # 获取第一行和第一列的标题（不包括"对象"）
        first_row = data.columns.tolist()
        first_col = data.index.tolist()

        # 根据排序后的学生和问题索引更新第一行和第一列
        sorted_first_row = [first_row[i] for i in sorted_problems_index if i in first_row]
        sorted_first_col = [first_col[i] for i in sorted_students_index if i in first_col]

        # 创建一个新的DataFrame来放置S-P表格和更新后的第一行和第一列
        sp_table = pd.DataFrame(index=sorted_first_col, columns=sorted_first_row)

        # 填充S-P表格数据
        for student in sorted_students_index:
            for problem in sorted_problems_index:
                sp_table.at[student, problem] = sorted_data.at[student, problem]

        # 显示排序后的S-P表格
        st.write("S-P 表格:")
        st.dataframe(sp_table)

if __name__ == '__main__':
    main()
