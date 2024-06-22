import streamlit as st
import pandas as pd

def calculate_coefficients(df):
    # 删除第一行和第一列
    df = df.iloc[1:, 1:]
    
    # 计算平均值和标准差
    average = df.mean()
    std_dev = df.std()

    # 计算差异系数（Coefficient of Variation）
    cv = std_dev / average

    # 计算注意系数，这里使用1 - 平均值，表示与平均表现的偏差
    attention_coefficient = 1 - average

    # 汇总计算结果
    summary = pd.DataFrame({
        'Average': average,
        'Standard Deviation': std_dev,
        'CV (Coefficient of Variation)': cv,
        'Attention Coefficient': attention_coefficient
    })

    return summary

def main():
    st.title('读取S-P 表格分析计算注意系数和差异系数')

    # 上传文件
    uploaded_file = st.file_uploader("上传一个xlsx或csv文件", type=["xlsx", "csv"])
    
    if uploaded_file is not None:
        try:
            # 根据文件类型读取数据
            if uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)

            st.write("上传的文件内容：")
            st.dataframe(df)

            # 计算注意系数和差异系数
            summary = calculate_coefficients(df)
            
            st.write("计算结果：")
            st.dataframe(summary)

        except Exception as e:
            st.error(f"文件处理时出错: {e}")

if __name__ == "__main__":
    main()
