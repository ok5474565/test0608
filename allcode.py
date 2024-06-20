import streamlit as st

# 导入子文件中的主函数
from newspachong666 import main as news_crawl_main
from count import main as count_main
from ciyuntu import main as ciyuntu_main
from app_bar2 import run as bar_chart_run  # 假设 run 函数是条形图的主函数
from app_abstract import main as summary_main  # 假设 main 函数是摘要的主函数
from app_worldcloud import run as wordcloud_run  # 假设 run 函数是词云图的主函数

# 设置页面配置
st.set_page_config(page_title="综合文本分析工具", layout="wide")

# 创建侧边栏
st.sidebar.title("功能选择")

# 创建下拉菜单供用户选择功能
function_options = [
    "新闻爬虫", 
    "高频词统计条形图", 
    "词云图生成", 
    "文本简要总结", 
    "词频统计条形图",  # 这个选项与上面的"高频词统计条形图"重复，根据实际功能调整
    "词频生成词云图"
]

selected_option = st.sidebar.selectbox(
    "选择一个功能:",
    function_options
)

# 根据用户选择的功能，调用相应的主函数
if selected_option == "新闻爬虫":
    news_crawl_main()
elif selected_option == "高频词统计条形图":
    count_main()
elif selected_option == "词云图生成":
    ciyuntu_main()
elif selected_option == "文本简要总结":
    summary_main()
elif selected_option == "词频统计条形图":
    bar_chart_run()
elif selected_option == "词频生成词云图":
    wordcloud_run()
else:
    st.sidebar.write("请选择一个有效选项。")
