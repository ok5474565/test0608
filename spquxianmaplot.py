import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('S-P 曲线图生成器')

# 上传文件
uploaded_file = st.file_uploader("上传得分统计表格 (.xlsx 文件)", type="xlsx")

if uploaded_file:
    # 读取 Excel 文件
    df = pd.read_excel(uploaded_file, header=1, index_col=0)
    
    # 统计每行和每列的得分计数
    row_sums = df.sum(axis=1)
    col_sums = df.sum(axis=0)
    
    # 将统计结果添加到 DataFrame 中
    df['总分'] = row_sums
    df.loc['总计'] = col_sums
    
    st.write('更新后的数据表格:')
    st.dataframe(df)
    
    # 计算 S-Curve 和 P-Curve
    s_curve = row_sums / df.shape[1]
    p_curve = col_sums / df.shape[0]
    
    # 排序
    s_curve = s_curve.sort_values(ascending=False)
    p_curve = p_curve.sort_values(ascending=True)
    
    # 绘制 S-P 曲线图
    plt.figure(figsize=(10, 6))
    
    s_curve_normalized_index = range(len(s_curve))
    p_curve_normalized_index = range(len(p_curve))
    
    plt.plot(s_curve_normalized_index, s_curve.values, 'r--', label='S 曲线 - 学生表现')
    plt.plot(p_curve_normalized_index, p_curve.values, 'b-', label='P 曲线 - 问题难度')
    
    plt.xlabel('索引')
    plt.ylabel('百分比')
    plt.title('S-P 曲线图')
    plt.legend()
    plt.tight_layout()
    
    st.pyplot(plt)
