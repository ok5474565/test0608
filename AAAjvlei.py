import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
import streamlit as st
import tempfile
import os
from matplotlib.font_manager import FontProperties

# 设置matplotlib支持中文显示
plt.rcParams['font.sans-serif'] = ['simhei']  # Windows系统使用SimHei字体
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
        plt.title('Hierarchical Clustering Dendrogram', fontsize=20)
        
        # 创建字体属性对象
        font_prop = FontProperties(fname='SimHei.ttf', size=14)
        
        # 绘制树状图并设置字体
        dendrobj = dendrogram(Z, labels=df.index)
        for i in range(len(dendrobj['ivl'])):
            plt.text(dendrobj['ivl'][i], dendrobj['h_yloc'][i] + 0.02,
                    str(round(dendrobj['d'][i], 3)),
                    rotate=90, va='bottom', fontproperties=font_prop)
        for i, d in enumerate(dendrobj['leaves']):
            plt.text(d, dendrobj['yloc'][d] - 0.1, df.index[i],
                    va='top', rotation=90, fontproperties=font_prop)
        
        plt.xlabel('Keywords', fontsize=14)
        plt.ylabel('Distance', fontsize=14)
        plt.xticks(rotation=90, fontsize=10)
        plt.tight_layout()  # 自动调整子图参数, 使之填充整个图像区域。
        
        # 保存图片到临时目录
        with tempfile.TemporaryDirectory() as tmpdirname:
            img_path = os.path.join(tmpdirname, 'hierarchical_clustering_dendrogram.png')
            plt.savefig(img_path)  # 指定保存路径和文件名
            plt.close()  # 关闭图形，避免在Streamlit中显示
            st.image(img_path, caption='Hierarchical Clustering Dendrogram', use_column_width=True)  # 显示图片

if __name__ == '__main__':
    main()
