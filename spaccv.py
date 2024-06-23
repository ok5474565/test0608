import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

def calculate_metrics(df):
    # 计算平均值（题目平均得分）
    avg_scores = df.mean()
    
    # 计算相关系数（学生答题情况与题目难度之间的关系）
    difficulties = 1 - avg_scores
    student_scores = df.sum(axis=1)
    correlation, _ = pearsonr(student_scores, difficulties)
    
    # 计算差异指数（反映学生答题情况的离散程度）
    variability_index = student_scores.var()
    
    # 计算同质性指数（评估学生群体在答题上是否具有相似性）
    homogeneity_index = df.var(axis=1).mean()
    
    # 计算项目注意系数（针对每个题目，衡量该题目对整体教学评价的影响程度）
    item_attention_index = df.var()
    
    # 计算学生注意系数（针对每个学生，衡量该学生在整体评价中的表现和问题）
    student_attention_index = df.var(axis=1)
    
    return avg_scores, correlation, variability_index, homogeneity_index, item_attention_index, student_attention_index

def main():
    st.title('S-P 表格分析工具')
    
    uploaded_file = st.file_uploader("上传一个 S-P 表格文件（xlsx 格式）", type="xlsx")
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file, header=1, index_col=0)
        
        avg_scores, correlation, variability_index, homogeneity_index, item_attention_index, student_attention_index = calculate_metrics(df)
        
        # 创建结果表格
        results = pd.DataFrame({
            '题目平均得分': avg_scores,
            '项目注意系数': item_attention_index
        })
        
        # 显示结果
        st.write("相关系数（学生答题情况与题目难度之间的关系）: ", correlation)
        st.write("差异指数（反映学生答题情况的离散程度）: ", variability_index)
        st.write("同质性指数（评估学生群体在答题上是否具有相似性）: ", homogeneity_index)
        st.write("学生注意系数（针对每个学生，衡量该学生在整体评价中的表现和问题）: ")
        st.write(student_attention_index)
        st.write("合并结果表格: ")
        st.write(results)
        
        # 提供下载按钮
        st.download_button(
            label="下载结果表格",
            data=results.to_excel(index=True, engine='openpyxl'),
            file_name='sp_results.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

if __name__ == "__main__":
    main()
