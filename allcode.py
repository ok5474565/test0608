import streamlit as st

# 导入其他文件中的主函数
from newspachong666 import main as news_crawl
from end11111 import main as end_main
from abc import run as abc_run

# 设置页面配置
st.set_page_config(page_title="综合文本分析工具", layout="wide")

# 创建侧边栏
st.sidebar.title("功能选择")

# 定义一个函数，用于显示应用程序
def show_app(choice):
    if choice == "新闻爬虫":
        news_crawl()
    elif choice == "文本分析工具":
        abc_run()
    elif choice == "高频词统计与词云图生成":
        end_main()
    else:
        st.sidebar.write("请选择一个有效选项。")

# 创建下拉菜单供用户选择功能
choice = st.sidebar.selectbox(
    "选择一个功能:",
    ("新闻爬虫", "文本分析工具", "高频词统计与词云图生成")
)

# 根据用户选择的功能，调用相应的函数
show_app(choice)
