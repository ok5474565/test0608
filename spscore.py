import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def main():
    st.title('S-P Chart and Analysis Tool')

    # 允许用户上传文件
    uploaded_file = st.file_uploader("Please upload your score statistics table (.xlsx)")
    
    if uploaded_file is not None:
        # 读取Excel文件
        data = pd.read_excel(uploaded_file)

        # 学生姓名是第一列的值（跳过标题"对象"）
        # 我们假设第一行是题目号码，第一列是学生姓名
        students = data.iloc[:, 0]  # 获取第一列所有值
        students = students[students != '对象']  # 排除标题"对象"

        # 题目号码是第一行的值，排除第一列（学生姓名）
        problems = data.index[:-1]  # 获取除最后一行的所有行名，假设最后一行是学生姓名

        # 构建DataFrame，排除标题"对象"
        sp_df = data.loc['P1':'P8']  # 假设列名是'P1'到'P8'

        # 计算每个学生的总分
        student_totals = sp_df.sum(axis=1)

        # 计算每个问题的总分
        problem_totals = sp_df.sum(axis=0)

        # 根据总分排序学生和问题
        sorted_students = student_totals.sort_values(ascending=False)
        sorted_problems = problem_totals.sort_values(ascending=False)

        # 根据总分排序S-P表
        sorted_sp_df = sp_df.loc[sorted_students.index, sorted_problems.index]

        # 显示S-P表格
        st.write("S-P Table:")
        st.table(sorted_sp_df)

        # 绘制S-P曲线
        s_curve = sorted_sp_df.mean(axis=1)
        p_curve = sorted_sp_df.mean(axis=0)

        plt.figure(figsize=(12, 8))
        plt.plot(s_curve, 'r--', label='S Curve - Student Performance')
        plt.plot(p_curve, 'b-', label='P Curve - Problem Difficulty')
        plt.title('Combined S and P Curves')
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
        average = sp_df.mean(numeric_only=True)
        std_dev = sp_df.std(numeric_only=True)
        cv = std_dev / average
        attention_coefficient = 1 - average.mean()

        # 汇总结果
        summary = pd.DataFrame({
            'Average': [average.mean()],
            'Standard Deviation': [std_dev.mean()],
            'CV (Coefficient of Variation)': [cv.mean()],
            'Attention Coefficient': [attention_coefficient]
        })
        st.write("Summary Statistics:")
        st.table(summary)

if __name__ == "__main__":
    main()
