import streamlit as st
import pandas as pd
import numpy as np

def main():
    st.title("S-P 表格分析")

    uploaded_file = st.file_uploader("上传一个 XLSX 文件", type=["xlsx"])
    
    if uploaded_file is not None:
        # 读取文件
        df = pd.read_excel(uploaded_file)
        
        # 获取题目名称
        question_names = list(df.columns[1:])
        
        # 去掉第一行（题目名称）和第一列（学生姓名）
        data = df.iloc[1:, 1:].astype(int)
        
        # 计算各题目的平均值和标准差
        means = data.mean(axis=0)
        std_devs = data.std(axis=0)
        
        # 计算 D 指数（区分指数）
        # 高分组和低分组
        high_group = data.iloc[:len(data)//3, :]
        low_group = data.iloc[-len(data)//3:, :]
        D_index = (high_group.mean(axis=0) - low_group.mean(axis=0)) / std_devs
        
        # 计算 P 指数（难度指数）
        P_index = 1 - means
        
        # 计算同质性指数（Homogeneity Index）
        homogeneity_index = std_devs / means
        
        # 汇总结果
        result_df = pd.DataFrame({
            "题目名称": question_names,
            "平均值": means,
            "标准差": std_devs,
            "区分指数 (D 指数)": D_index,
            "难度指数 (P 指数)": P_index,
            "同质性指数": homogeneity_index
        })
        
        st.write("计算结果：")
        st.dataframe(result_df)

if __name__ == "__main__":
    main()
