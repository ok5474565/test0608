import streamlit as st
import pandas as pd
import numpy as np

def main():
    st.title("S-P 表格分析应用")

    uploaded_file = st.file_uploader("请上传 xlsx 文件", type="xlsx")

    if uploaded_file:
        df = pd.read_excel(uploaded_file)

        # 获取题目名称（第一行）和学生姓名（第一列）
        question_names = df.columns[1:].tolist()
        student_names = df.iloc[:, 0].tolist()

        # 仅保留答题数据（去掉第一行和第一列）
        answer_data = df.iloc[:, 1:].values
        
        # 计算题目的平均值和标准差
        mean_scores = answer_data.mean(axis=0)
        std_scores = answer_data.std(axis=0)

        # 计算 P 指数（题目难度）
        p_index = 1 - mean_scores

        # 计算 D 指数（区分度）
        total_scores = answer_data.sum(axis=1)
        sorted_indices = np.argsort(total_scores)[::-1]
        high_group_size = int(len(total_scores) * 0.27)
        low_group_size = high_group_size

        high_group = answer_data[sorted_indices[:high_group_size], :]
        low_group = answer_data[sorted_indices[-low_group_size:], :]

        high_group_mean = high_group.mean(axis=0)
        low_group_mean = low_group.mean(axis=0)
        d_index = high_group_mean - low_group_mean

        # 计算同质性指数
        homogeneity_index = 1 - std_scores

        # 构建结果 DataFrame
        results_df = pd.DataFrame({
            '题目名称': question_names,
            '平均值': mean_scores,
            '标准差': std_scores,
            '注意系数（D指数）': d_index,
            '差异系数（P指数）': p_index,
            '同质性指数': homogeneity_index
        })

        st.write("分析结果：")
        st.dataframe(results_df)

if __name__ == "__main__":
    main()
