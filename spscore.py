import pandas as pd
import streamlit as st

def read_and_process_xlsx(file):
    # 读取Excel文件，跳过第一行和第一列
    df = pd.read_excel(file, engine='openpyxl', header=1, skiprows=1)
    
    # 确保所有数据都是数值类型
    df = df.stack().fillna(0).unstack().astype(int)
    
    return df

def calculate_totals(df):
    # 计算每个学生的总分
    student_totals = df.sum(axis=1)
    
    # 计算每个问题的总分
    problem_totals = df.sum(axis=0)
    
    return student_totals, problem_totals

def sort_students_by_totals(student_totals, problem_totals):
    # 根据总分排序学生，如果总分相同，则使用问题得分向量与学生得分向量的协方差进行排序
    sorted_students = student_totals.sort_values(ascending=False)
    # 如果有并列，可以使用协方差作为第二排序标准
    # sorted_students = sorted_students[~student_totals.duplicated(keep='first')]
    return sorted_students.index

def sort_problems_by_totals(problem_totals):
    # 根据总分排序问题
    sorted_problems = problem_totals.sort_values(ascending=False)
    return sorted_problems.index

def main():
    st.title('学生成绩排序应用')
    
    # 让用户上传Excel文件
    uploaded_file = st.file_uploader("上传你的Excel文件", type=["xlsx"])
    
    if uploaded_file is not None:
        # 读取和处理数据
        df = read_and_process_xlsx(uploaded_file)
        
        # 计算总分
        student_totals, problem_totals = calculate_totals(df)
        
        # 排序学生
        sorted_students_index = sort_students_by_totals(student_totals, problem_totals)
        
        # 排序问题
        sorted_problems_index = sort_problems_by_totals(problem_totals)
        
        # 根据排序后的索引重新排列DataFrame
        sorted_df = df.loc[sorted_students_index, sorted_problems_index]
        
        # 显示排序后的学生成绩表
        st.write("排序后的学生成绩表:")
        st.dataframe(sorted_df)
        
        # 显示问题总分
        st.write("问题总分:")
        st.dataframe(pd.DataFrame(problem_totals, index=sorted_problems_index, columns=['问题总分']))
        
        # 显示学生总分
        st.write("学生总分:")
        st.dataframe(pd.DataFrame(student_totals, index=sorted_students_index, columns=['学生总分']))

if __name__ == '__main__':
    main()
