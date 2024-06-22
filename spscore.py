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
            data = data.iloc[1:]  # 移除第一行
            data.columns = data.columns.str.strip()  # 清理列名中的空格

        # 计算每个学生的总分
        student_totals = data.sum(axis=1)

        # 计算每个问题的总分
        problem_totals = data.sum(axis=0)

        # 根据学生总分和问题总分排序
        sorted_students = student_totals.sort_values(ascending=False)
        sorted_problems = problem_totals.sort_values(ascending=False)

        # 根据总分排序DataFrame
        sorted_data = data.loc[sorted_students.index, sorted_problems.index]

        # 显示排序后的DataFrame
        st.write("S-P 表格:")
        st.write(sorted_data)

        # TODO: 曲线图和系数计算可以根据需要添加

# 运行主函数
if __name__ == '__main__':
    main()
