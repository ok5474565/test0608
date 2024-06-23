import streamlit as st

# 导入子文件中的主函数
from newspachong666 import main as news_crawl_main          # 新闻爬虫
from app_abstract import main as summary_main               # 爬虫生成摘要
from app_bar2 import run as bar_chart_run                   # 爬虫生成条形图
from app_worldcloud import run as wordcloud_run             # 爬虫生成词云图

from tiaoxingtuall import main as tiaoxingtuall_main        # 上传文件生成条形图
from ciyuntuall import main as ciyuntuall_main              # 上传文件生成词云图

from spscore import main as spscore_main                    # 上传文件生成S-P表格
from sppic import main as sppic_main                        # 上传S-P表格生成S-P曲线maplot
from sppicecharts import main as sppicecharts_main          # 上传S-P表格生成S-P曲线echart
from spaccv import main as spaccv_main                      # 计算注意系数和差异系数

# from tiaoxingtuend import main as text_analysis_main  # 假设主函数名为main
# from ciyuntuend import main as wordcloud_main  # 假设主函数名为main

# from count import main as count_main
# from ciyuntu import main as ciyuntu_main
# from count3 import main as count3_main  # 新增：读取GBK CSV生成条形图
# from count1 import main as count1_main  # 新增：读取UTF-8 CSV生成条形图
# from ciyuntu3 import main as ciyuntu3_main  # 新增：读取GBK CSV生成词云图
# from ciyuntu777 import main as ciyuntu777_main  # 新增：读取UTF-8 CSV生成词云图

# 设置页面配置
st.set_page_config(page_title="综合文本分析工具", layout="wide")

# 创建侧边栏
st.sidebar.title("功能选择")

# 创建下拉菜单供用户选择功能
function_options = [
    "新闻爬虫",
    "文本简要总结",
    "输入链接爬取内容统计词频条形图",
    "输入链接爬取内容生成词云图",
    # "在线文本分词与高频词统计小程序",  # 新增功能名称
    # "在线文本分词与词云图生成小程序",  # 新增功能名称
    # "读取txt统计高频词生成条形图",
    # "读取txt生成词云图",
    # "读取GBK CSV生成条形图",  # 新增选项：count1.py
    # "读取UTF-8 CSV生成条形图",  # 新增选项：count1.py
    # "读取GBK CSV生成词云图",  # 新增选项：ciyuntu3.py
    # "读取UTF-8 CSV生成词云图"  # 新增选项：ciyuntu777.py
]

selected_option = st.sidebar.selectbox(
    "选择一个功能:",
    function_options
)

# 根据用户选择的功能，调用相应的主函数
if selected_option == "新闻爬虫":
    news_crawl_main()
elif selected_option == "文本简要总结":
    summary_main()
elif selected_option == "输入链接爬取内容统计词频条形图":
    bar_chart_run()
elif selected_option == "输入链接爬取内容生成词云图":
    wordcloud_run()



# elif selected_option == "在线文本分词与高频词统计小程序":
#     text_analysis_main()
# elif selected_option == "在线文本分词与词云图生成小程序":
#     wordcloud_main()
# elif selected_option == "读取txt统计高频词生成条形图":
#     count_main()
# elif selected_option == "读取txt生成词云图":
#     ciyuntu_main()
# elif selected_option == "读取GBK CSV生成条形图":  # 新增选项的处理逻辑
#     count3_main()
# elif selected_option == "读取UTF-8 CSV生成条形图":  # 新增选项的处理逻辑
#     count1_main()
# elif selected_option == "读取GBK CSV生成词云图":  # 新增选项的处理逻辑
#     ciyuntu3_main()
# elif selected_option == "读取UTF-8 CSV生成词云图":  # 新增选项的处理逻辑
#     ciyuntu777_main()
else:
    st.sidebar.write("请选择一个有效选项。")
