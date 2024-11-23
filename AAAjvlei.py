import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
import streamlit as st
import io

# 设置matplotlib支持中文显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 使用Arial Unicode MS，这在大多数环境中都可用
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

def main():
    # 用户上传文件
    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx'])
    
    if uploaded_file is not None:
        # 读取上传的Excel文件
        df = pd.read_excel(uploaded_file, index_col=0)
        
        # 将缺失值填充为0
        df.fillna(0, inplace=True)
        
        # 进行层次聚类
        # 计算距离矩阵，这里使用欧式距离
        dist_matrix = pdist(df, metric='euclidean')
        
        # 进行层次聚类，这里使用ward方法
        Z = linkage(dist_matrix, method='ward')
        
        # 绘制树状图
        plt.figure(figsize=(36, 18))  # 进一步增加图形的宽度和高度
        plt.title('Hierarchical Clustering Dendrogram', fontsize=20)
        plt.xlabel('Keywords', fontsize=14)  # 适当减小字体大小
        plt.ylabel('Distance', fontsize=14)
        dendrogram(Z, labels=df.index)  # 绘制树状图
        plt.xticks(rotation=90, fontsize=10)  # 适当减小字体大小
        plt.tight_layout()  # 自动调整子图参数, 使之填充整个图像区域。
        
        # 将图像保存到一个字节流中
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        
        # 使用Streamlit显示图像
        st.image(img_buffer, caption='Hierarchical Clustering Dendrogram', use_column_width=True)
        
        # 关闭图形，避免在Streamlit中显示
        plt.close()

if __name__ == '__main__':
    main()
