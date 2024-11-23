import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
import streamlit as st
import tempfile
import os
from matplotlib.font_manager import FontProperties

# 设置matplotlib支持中文显示
# 尝试加载SimHei字体，如果加载失败则使用默认字体
font_path = 'simHei.ttf'  # 指定字体文件路径
font_prop = FontProperties(fname=font_path, size=14)
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 创建Streamlit应用
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
        plt.title('Hierarchical Clustering Dendrogram', fontsize=20, fontproperties=font_prop)
        plt.xlabel('Keywords', fontsize=14, fontproperties=font_prop)  # 适当减小字体大小
        plt.ylabel('Distance', fontsize=14, fontproperties=font_prop)
        dendrogram(Z, labels=df.index, fontproperties=font_prop)  # 绘制树状图
        plt.xticks(rotation=90, fontsize=10, fontproperties=font_prop)  # 适当减小字体大小
        plt.tight_layout()  # 自动调整子图参数, 使之填充整个图像区域。
        
        # 保存图片到临时目录
        with tempfile.TemporaryDirectory() as tmpdirname:
            img_path = os.path.join(tmpdirname, 'hierarchical_clustering_dendrogram.png')
            plt.savefig(img_path)  # 指定保存路径和文件名
            plt.close()  # 关闭图形，避免在Streamlit中显示
            st.image(img_path, caption='Hierarchical Clustering Dendrogram', use_column_width=True)  # 显示图片

if __name__ == '__main__':
    main()
