import pandas as pd
import streamlit as st
from echarts.charts import Bar
from echarts import Options

# 读取Excel文件
def read_excel(file_path):
    return pd.read_excel(file_path)

# 统计得分并添加到DataFrame
def calculate_scores(df):
    # 忽略第一行和第一列
    df = df.iloc[1:, 1:]
    # 计算每列的得分
    column_scores = df.sum(axis=0)
    # 计算每行的得分
    row_scores = df.sum(axis=1)
    # 将列得分添加到DataFrame
    df['Total'] = column_scores
    # 将行得分添加到DataFrame
    df.loc['Average'] = row_scores.mean()
    return df

# 绘制S-P曲线图
def plot_sp_curve(df):
    # 这里假设我们使用Bar来绘制，实际上echarts-python可能需要调整以适应S-P曲线
    chart = Bar(init_opts=Options(width="1000px", height="600px"))
    chart.add_xaxis(df.index.tolist())
    chart.add_yaxis("Scores", df['Total'].tolist())
    chart.add_yaxis("Average", [df.loc['Average']]*len(df))
    return chart

# Streamlit界面
def main():
    st.title("S-P Curve Generator")
    
    # 上传Excel文件
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])
    
    if uploaded_file is not None:
        # 读取文件
        df = read_excel(uploaded_file)
        
        # 计算得分并更新DataFrame
        df = calculate_scores(df)
        
        # 绘制S-P曲线图
        sp_curve = plot_sp_curve(df)
        
        # 显示DataFrame
        st.write(df)
        
        # 显示S-P曲线图
        st.pyplot(sp_curve.render_embed())

if __name__ == "__main__":
    main()
