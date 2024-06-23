import streamlit as st
import pandas as pd
import numpy as np

def main():
    st.title("S-P 表格分析")

    uploaded_file = st.file_uploader("上传 XLSX 文件", type="xlsx")

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file, header=None)
        df = df.iloc[1:, 1:]  # 跳过第一行和第一列
        
        st.write("原始数据")
        st.dataframe(df)

        # 计算各个题目的平均值和标准差
        means = df.mean(axis=0)
        stds = df.std(axis=0)
        
        # 计算差异系数（P指数）
        p_indexes = 1 - means

        # 计算注意系数（D指数）
        high_group = df.loc[df.sum(axis=1) >= df.sum(axis=1).median()]
        low_group = df.loc[df.sum(axis=1) < df.sum(axis=1).median()]
        d_indexes = high_group.mean(axis=0) - low_group.mean(axis=0)

        # 计算同质性指数（基于所有学生回答的标准差）
        homogeneity_indexes = df.std(axis=1).mean()

        # 生成题目号
        question_numbers = [f'题目{idx+1}' for idx in range(df.shape[1])]

        # 汇总结果
        results = pd.DataFrame({
            '题目号': question_numbers,
            '平均值': means,
            '标准差': stds,
            'D指数': d_indexes,
            'P指数': p_indexes
        })

        st.write("计算结果")
        st.dataframe(results)

        st.write(f"同质性指数: {homogeneity_indexes}")

if __name__ == "__main__":
    main()
