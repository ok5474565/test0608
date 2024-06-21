import streamlit as st

# 导入子文件中的主函数
from newspachong666 import main as news_crawl_main
from count import main as count_main
from ciyuntu import main as ciyuntu_main
from app_bar2 import run as bar_chart_run  
from app_abstract import main as summary_main  
from app_worldcloud import run as wordcloud_run  
from count1 import main as count1_main  # 新增：读取CSV生成条形图
from ciyuntu3 import main as ciyuntu3_main  # 新增：读取GBK CSV生成词云图
from ciyuntu777 import main as ciyuntu777_main  # 新增：读取UTF-8 CSV生成词云图

# 设置页面配置
st.set_page_config(page_title="综合文本分析工具", layout="wide")

# 创建侧边栏
st.sidebar.title("功能选择")

# 创建下拉菜单供用户选择功能
function_options = [
    "新闻爬虫",
    "读取txt统计高频词生成条形图",
    "读取txt生成词云图",
    "文本简要总结",
    "输入链接爬取内容统计词频条形图",
    "输入链接爬取内容生成词云图",
    "读取UTF-8 CSV生成条形图",  # 新增选项：count1.py
    "读取GBK CSV生成词云图",  # 新增选项：ciyuntu3.py
    "读取UTF-8 CSV生成词云图"  # 新增选项：ciyuntu777.py
]

selected_option = st.sidebar.selectbox(
    "选择一个功能:",
    function_options
)

# 根据用户选择的功能，调用相应的主函数
if selected_option == "新闻爬虫":
    news_crawl_main()
elif selected_option == "读取txt统计高频词生成条形图":
    count_main()
elif selected_option == "读取txt生成词云图":
    ciyuntu_main()
elif selected_option == "文本简要总结":
    summary_main()
elif selected_option == "输入链接爬取内容统计词频条形图":
    bar_chart_run()
elif selected_option == "输入链接爬取内容生成词云图":
    wordcloud_run()
elif selected_option == "读取UTF-8 CSV生成条形图":  # 新增选项的处理逻辑
    count1_main()
elif selected_option == "读取GBK CSV生成词云图":  # 新增选项的处理逻辑
    ciyuntu3_main()
elif selected_option == "读取UTF-8 CSV生成词云图":  # 新增选项的处理逻辑
    ciyuntu777_main()
else:
    st.sidebar.write("请选择一个有效选项。")
