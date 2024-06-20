import streamlit as st
from newspachong666 import main as news_crawl
from end11111 import main as end_main  # 修改：直接导入end11111.py的main函数
from abc import main as abc_main  # 修改：导入abc.py的main函数

# 设置页面配置
st.set_page_config(page_title="综合文本分析工具", layout="wide")

# 创建侧边栏
st.sidebar.title("功能选择")

# 定义一个函数，用于显示应用程序
def show_app(choice):
    if choice == "新闻爬虫":
        news_crawl()
    elif choice == "文本分析工具":
        abc_main()  # 调用abc.py中的main函数
    elif choice == "高频词统计与词云图生成":
        end_main()  # 调用end11111.py中的main函数
    else:
        st.sidebar.write("请选择一个有效选项。")

# 创建下拉菜单供用户选择功能
choice = st.sidebar.selectbox(
    "选择一个功能:",
    ("新闻爬虫", "文本分析工具", "高频词统计与词云图生成")
)

# 根据用户选择的功能，调用相应的函数
show_app(choice)
