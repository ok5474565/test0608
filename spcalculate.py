import streamlit as st
import pandas as pd
import numpy as np

def calculate_statistics(df):
    # 将行列转置
    df = df.transpose()
    df.columns = df.iloc[0]
    df = df[1:]

    # 计算平均值和标准差
    mean_values = df.mean()
    std_values = df.std()

    # 计算D指数和P指数
    p_index = df.mean(axis=0)
    d_index = df.apply(lambda x: np.corrcoef(x, df.mean(axis=1))[0, 1])

    # 计算相关系数和同质性指数
    correlation_matrix = df.corr()
    homogeneity_index = correlation_matrix.mean().mean()

    return mean_values, std_values, d_index, p_index, correlation_matrix, homogeneity_index

def main():
    st.title("S-P 表格分析工具")

    uploaded_file = st.file_uploader("上传一个表格文件", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            # 移除第一行和第一列
            df = df.drop(df.columns[0], axis=1)
            df = df.drop(df.index[0])

            st.write("原始数据表：")
            st.dataframe(df)

            mean_values, std_values, d_index, p_index, correlation_matrix, homogeneity_index = calculate_statistics(df)

            result_df = pd.DataFrame({
                "平均值": mean_values,
                "标准差": std_values,
                "D指数（区分度）": d_index,
                "P指数（难度）": p_index
            })

            st.write("计算结果：")
            st.dataframe(result_df)

            st.write("相关系数矩阵：")
            st.dataframe(correlation_matrix)

            st.write("同质性指数：")
            st.write(homogeneity_index)

        except Exception as e:
            st.error(f"处理文件时出错: {e}")

if __name__ == "__main__":
    main()
