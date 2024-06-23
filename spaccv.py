import streamlit as st
import pandas as pd
import numpy as np

# Function to calculate the required metrics
def calculate_metrics(df):
    # Drop the first row and first column
    data = df.iloc[1:, 1:]
    # Convert data to numeric
    data = data.apply(pd.to_numeric)
    
    # Calculate average and standard deviation
    avg = data.mean(axis=0)
    std_dev = data.std(axis=0)
    
    # Calculate caution index (1 - average score)
    caution_index = 1 - avg
    
    # Calculate difference index (standard deviation / average score)
    difference_index = std_dev / avg
    
    # Combine results into a single DataFrame
    summary = pd.DataFrame({
        'Average': avg,
        'Standard Deviation': std_dev,
        'Caution Index': caution_index,
        'Difference Index': difference_index
    })
    
    return summary

# Function to convert DataFrame to Excel
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

def main():
    st.title('S-P表格分析工具')

    # File upload
    uploaded_file = st.file_uploader("上传S-P表格文件（xlsx或csv格式）", type=["xlsx", "csv"])

    if uploaded_file is not None:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        
        # Display the uploaded file
        st.write("上传的表格数据:")
        st.write(df)
        
        # Calculate metrics
        summary = calculate_metrics(df)
        
        # Display the results
        st.write("计算结果:")
        st.write(summary)
        
        # Add a download button for Excel file
        excel_data = convert_df_to_excel(summary)
        
        st.download_button(
            label="下载结果Excel文件",
            data=excel_data,
            file_name='summary.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

if __name__ == '__main__':
    main()
