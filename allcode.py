import streamlit as st
from newspachong666 import main as news_crawl
from abc import run as abc_run

# 设置页面配置
st.set_page_config(page_title="综合文本分析工具", layout="wide")

# 创建侧边栏
st.sidebar.title("功能选择")

# 定义一个函数，用于运行end11111.py中的逻辑
def run_end11111():
    import streamlit as st
    # 此处直接运行end11111.py文件中的代码
    st.sidebar.title("功能选择")
    choice = st.sidebar.selectbox(
        "选择一个功能:",
        ("高频词统计条形图", "词云图生成")
    )
    if choice == "高频词统计条形图":
        from count import main as count_main
        count_main()
    elif choice == "词云图生成":
        from ciyuntu import main as ciyuntu_main
        ciyuntu_main()
    else:
        st.sidebar.write("请选择一个有效选项。")

# 创建下拉菜单供用户选择功能
function_options = [
    "新闻爬虫",
    "文本分析工具",
    "高频词统计与词云图生成"
]

selected_option = st.sidebar.selectbox(
    "选择一个功能:",
    function_options
)

# 根据用户选择的功能，调用相应的函数
if selected_option == "新闻爬虫":
    news_crawl()
elif selected_option == "文本分析工具":
    abc_run()
elif selected_option == "高频词统计与词云图生成":
    run_end11111()
else:
    st.sidebar.write("请选择一个有效选项。")
