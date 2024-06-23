import streamlit as st
import pandas as pd
import numpy as np

def calc_correlation(df):
    question_difficulty = df.mean(axis=0)
    student_scores = df.mean(axis=1)
    return student_scores.corr(question_difficulty)

def calc_variance_index(df):
    return df.var(axis=1).mean()

def calc_homogeneity_index(df):
    return 1 - df.var(axis=0).mean()

def calc_item_attention_index(df):
    return df.var(axis=0)

def calc_student_attention_index(df):
    return df.mean(axis=1)

def main():
    st.title('S-P表格分析')

    uploaded_file = st.file_uploader('上传你的xlsx或csv文件', type=['xlsx', 'csv'])

    if uploaded_file:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        st.write('原始数据:')
        st.dataframe(df)

        df = df.iloc[1:, 1:].astype(int)

        correlation = calc_correlation(df)
        variance_index = calc_variance_index(df)
        homogeneity_index = calc_homogeneity_index(df)
        item_attention_index = calc_item_attention_index(df)
        student_attention_index = calc_student_attention_index(df)

        results = pd.DataFrame({
            '相关系数': [correlation],
            '差异指数': [variance_index],
            '同质性指数': [homogeneity_index]
        })

        item_attention_index = item_attention_index.rename('项目注意系数')
        student_attention_index = student_attention_index.rename('学生注意系数')

        st.write('分析结果:')
        st.dataframe(results)

        st.write('项目注意系数:')
        st.dataframe(item_attention_index)

        st.write('学生注意系数:')
        st.dataframe(student_attention_index)

        download_df = pd.concat([results, item_attention_index, student_attention_index], axis=1)
        
        csv = download_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="下载结果 CSV",
            data=csv,
            file_name='分析结果.csv',
            mime='text/csv',
        )

if __name__ == '__main__':
    main()
