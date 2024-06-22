# 导入所需的库
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# 创建Streamlit应用
def main():
    # 设置页面的标题
    st.title('S-P Chart and Analysis Tool')

    # 允许用户上传文件
    uploaded_file = st.file_uploader("Please upload your score statistics table (.xlsx)", type=["xlsx"])

    # 如果用户上传了文件，则进行处理
    if uploaded_file is not None:
        # 读取Excel文件
        data = pd.read_excel(uploaded_file)

        # 构建DataFrame
        sp_df = pd.pivot_table(data, values='得分', index=['学生姓名'], columns=['题目号码'], aggfunc='first')

        # 计算每个学生的总分和每个问题的总分
        student_totals = sp_df.sum(axis=1)
        problem_totals = sp_df.sum(axis=0)

        # 根据总分排序学生和问题
        sorted_students_index = student_totals.sort_values(ascending=False).index
        sorted_problems_index = problem_totals.sort_values(ascending=False).index

        # 根据总分排序S-P表
        sorted_sp_df = sp_df.loc[sorted_students_index, sorted_problems_index]

        # 显示S-P表格
        st.write("S-P Table:")
        st.table(sorted_sp_df)

        # 计算S-P曲线
        s_curve = sorted_sp_df.mean(axis=1).sort_values(ascending=False)
        p_curve = sorted_sp_df.mean(axis=0).sort_values(ascending=True)

        # 绘制S-P曲线
        plt.figure(figsize=(12, 8))
        plt.plot(s_curve.index, s_curve.values, 'r--', label='S Curve - Student Performance')
        plt.plot(p_curve.index, p_curve.values, 'b-', label='P Curve - Problem Difficulty')
        plt.title('Combined S and P Curves')
        plt.xlabel('Index')
        plt.ylabel('Percentage')
        plt.legend()
        plt.tight_layout()

        # 将图表转换为图片格式以在Streamlit中显示
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        st.image(buf, caption='S-P Curves', use_column_width=True)

        # 计算差异系数和注意系数
        average = sp_df.mean()
        std_dev = sp_df.std()
        cv = std_dev / average
        attention_coefficient = 1 - average

        # 汇总计算结果
        summary = pd.DataFrame({
            'Average': average,
            'Standard Deviation': std_dev,
            'CV (Coefficient of Variation)': cv,
            'Attention Coefficient': attention_coefficient
        })
        st.write("Summary Statistics:")
        st.table(summary)

# 运行主函数
if __name__ == "__main__":
    main()
