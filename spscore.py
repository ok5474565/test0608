import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

def main():
    st.title('S-P Chart and Analysis Tool')

    # 允许用户上传文件
    uploaded_file = st.file_uploader("Please upload your score statistics table (.xlsx)", type=["xlsx"])
    
    if uploaded_file is not None:
        # 读取Excel文件
        data = pd.read_excel(uploaded_file)
        
        # 获取学生姓名和题目号码
        students = data.columns[1:]  # 假设第一列是"对象"，从第二列开始是学生姓名
        problems = data.index[1:]  # 假设第一行是题目号码，从第二行开始是数据

        # 构建S-P DataFrame
        sp_df = data[students]  # 选择除了"对象"列以外的数据

        # 计算每个学生的总分和每个问题的总分
        student_totals = sp_df.sum(axis=1)
        problem_totals = sp_df.sum(axis=0)

        # 根据总分排序学生和问题
        sorted_students = student_totals.sort_values(ascending=False).index
        sorted_problems = problem_totals.sort_values(ascending=False).index

        # 根据总分排序S-P表
        sorted_sp_df = sp_df.loc[sorted_students, sorted_problems]

        # 显示S-P表格
        st.write("S-P Table:")
        st.table(sorted_sp_df)

        # 计算S-P曲线
        s_curve = student_totals.sort_values(ascending=False)
        p_curve = problem_totals.sort_values(ascending=False)

        # 绘制S-P曲线
        plt.figure(figsize=(12, 8))
        plt.plot(s_curve, 'r--', label='S Curve - Student Performance')
        plt.plot(p_curve, 'b-', label='P Curve - Problem Difficulty')
        plt.title('Combined S and P Curves')
        plt.xlabel('Index')
        plt.ylabel('Score')
        plt.legend()
        plt.xticks(rotation=45)  # 旋转X轴标签以便阅读
        plt.tight_layout()

        # 将图表转换为图片格式以在Streamlit中显示
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        st.image(buf, caption='S-P Curves', use_column_width=True)

        # 计算差异系数和注意系数
        average = sp_df.mean(numeric_only=True)
        std_dev = sp_df.std(numeric_only=True)
        cv = std_dev / average
        attention_coefficient = 1 - average.mean()

        # 汇总计算结果
        summary = pd.DataFrame({
            'Average': average,
            'Standard Deviation': std_dev,
            'CV (Coefficient of Variation)': cv,
            'Attention Coefficient': attention_coefficient
        })
        st.write("Summary Statistics:")
        st.table(summary)

if __name__ == "__main__":
    main()
