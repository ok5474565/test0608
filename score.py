import streamlit as st

# 导入子文件中的主函数
from paqutiaoxingtu import run as paqutiaoxingtu_run
from paqucloud import run as paqucloud_run

from tiaoxingtuall import main as tiaoxingtuall_main
from ciyuntuall import main as ciyuntuall_main

from spscore import main as spscore_main
from sppic import main as sppic_main
from sppicecharts import main as sppicecharts_main
from spcalculate import main as spcalculate_main

def main():
    st.title("学生成绩分析工具")
    
    # 设置页面配置
    #st.set_page_config(page_title="学生成绩分析工具", layout="wide")

    # 创建侧边栏
    st.sidebar.title("功能选择")

    # 创建下拉菜单供用户选择功能
    function_options = [
        #"输入链接爬取内容统计词频条形图",
        #"输入链接爬取内容生成词云图",
        "在线文本分词与高频词统计",
        "在线文本分词与词云图生成",
        "根据得分统计表制作S - P表格",
        "根据S-P表格使用maplotlib绘制S-P曲线",
        "根据S-P表格使用echarts绘制S-P曲线",
        "根据表格计算注意系数、差异系数"
    ]

    selected_option = st.sidebar.selectbox(
        "选择一个功能:",
        function_options
    )

    # 根据用户选择的功能，调用相应的主函数
    if selected_option == "在线文本分词与高频词统计":
        tiaoxingtuall_main()
    elif selected_option == "在线文本分词与词云图生成":
        ciyuntuall_main()
    elif selected_option == "根据得分统计表制作S - P表格":
        spscore_main()
    elif selected_option == "根据S-P表格使用maplotlib绘制S-P曲线":
        sppic_main()
    elif selected_option == "根据S-P表格使用echarts绘制S-P曲线":
        sppicecharts_main()
    elif selected_option == "根据表格计算注意系数、差异系数":
        spcalculate_main()
    else:
        st.sidebar.write("请选择一个有效选项。")

if __name__ == "__main__":
    main()
