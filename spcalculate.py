import streamlit as st
import pandas as pd
import numpy as np

def main():
    st.title("S-P 表格分析")

    # 上传文件
    uploaded_file = st.file_uploader("上传一个 Excel 文件", type="xlsx")

    if uploaded_file is not None:
        # 读取Excel文件
        df = pd.read_excel(uploaded_file)
        
        # 获取题目名称和学生姓名
        question_names = df.columns[1:]
        student_names = df.iloc[:, 0]
        
        # 获取答题数据
        data = df.iloc[:, 1:].values

        # 计算每题的平均值和标准差
        mean_scores = np.mean(data, axis=0)
        std_devs = np.std(data, axis=0)
        
        # 计算注意系数、差异系数和同质性指数
        discrimination_coefficient = 1 - np.var(data, axis=0) / np.mean(data, axis=0)
        variation_coefficient = std_devs / mean_scores
        homogeneity_index = 1 - std_devs / np.sqrt(mean_scores * (1 - mean_scores))

        # 汇总计算结果
        results = pd.DataFrame({
            "题目名称": question_names,
            "平均值": mean_scores,
            "标准差": std_devs,
            "注意系数": discrimination_coefficient,
            "差异系数": variation_coefficient,
            "同质性指数": homogeneity_index
        })

        # 显示结果表格
        st.write("计算结果：")
        st.dataframe(results)

if __name__ == "__main__":
    main()
