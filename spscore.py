import streamlit as st
import pandas as pd

# Streamlit界面设置
def main():
    st.title('学生得分统计与S-P表格生成')

    # 用户上传文件
    uploaded_file = st.file_uploader("请上传您的 Excel 文件 (.xlsx)", type=["xlsx"])
    if uploaded_file is not None:
        # 读取文件
        data = pd.read_excel(uploaded_file)

        # 取第一行作为题目（列名），同时跳过第一列（通常是"对象"或其他标题）
        col_names = data.iloc[1]  # 直接取第二行作为列名

        # 转置数据，使第一列成为学生姓名（索引）
        data = data.iloc[:, 1:].transpose()  # 取第二列及之后的列进行转置

        # 由于转置后，原来的第一列变成了索引，我们将其设置为列名
        data.columns = col_names

        # 计算每个学生的总分
        student_totals = data.sum(axis=1)

        # 计算每个问题的总分
        problem_totals = data.sum(axis=0)

        # 根据总分排序学生索引和问题索引
        sorted_students_index = student_totals.sort_values(ascending=False).index
        sorted_problems_index = problem_totals.sort_values(ascending=False).index

        # 根据总分排序DataFrame
        sorted_data = data.loc[sorted_students_index, sorted_problems_index]

        # 显示排序后的DataFrame
        st.write("S-P 表格:")
        st.dataframe(sorted_data)

# 运行主函数
if __name__ == '__main__':
    main()
