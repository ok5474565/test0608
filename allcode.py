import streamlit as st

# 导入子文件中的主函数
from newspachong666 import main as news_crawl_main  # 新闻爬虫
from count import main as count_main  # 读取txt生成条形图
from ciyuntu import main as ciyuntu_main  # 读取txt生成词云图
from count1 import main as count_main  # 读取CSV生成条形图
from ciyuntu3 import main as ciyuntu_gbk_main  # 读取GBK CSV生成词云图
from ciyuntu777 import main as ciyuntu_utf8_main  # 读取UTF-8 CSV生成词云图
from app_bar2 import run as bar_chart_run  # 爬取网页内容生成条形图
from app_abstract import main as summary_main  # 爬取网页内容撰写摘要
from app_worldcloud import run as wordcloud_run  # 爬取网页内容生成词云图


# 设置页面配置
st.set_page_config(page_title="综合文本分析工具", layout="wide")

# 创建侧边栏
st.sidebar.title("功能选择")

# 创建下拉菜单供用户选择功能
function_options = [
    "新闻爬虫",
    "读取txt统计高频词生成条形图",  # 假设这是原有选项之一
    "读取txt生成词云图",  # 假设这是原有选项之一
    "文本简要总结",  # 假设这是原有选项之一
    "输入链接爬取内容统计词频条形图",  # 假设这是原有选项之一
    "输入链接爬取内容生成词云图",  # 假设这是原有选项之一
    "读取CSV生成条形图",  # count1.py 新增选项
    "读取GBK CSV生成词云图",  # ciyuntu3.py 新增选项
    "读取UTF-8 CSV生成词云图"  # ciyuntu777.py 新增选项
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
elif selected_option == "读取CSV生成条形图":
    count_main()
elif selected_option == "读取GBK CSV生成词云图":
    ciyuntu_gbk_main()
elif selected_option == "读取UTF-8 CSV生成词云图":
    ciyuntu_utf8_main()
# ... 其他原有选项的处理逻辑
else:
    st.sidebar.write("请选择一个有效选项。")
