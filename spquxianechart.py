import streamlit as st
import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts
from streamlit_echarts import st_echarts

def main():
    st.title('S-P 曲线图生成器')
    
    uploaded_file = st.file_uploader("上传得分统计表格 (.xlsx 文件)", type="xlsx")
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file, header=1, index_col=0)
        row_sums = df.sum(axis=1)
        col_sums = df.sum(axis=0)
        df['总分'] = row_sums
        df.loc['总计'] = col_sums
        
        st.write('更新后的数据表格:')
        st.dataframe(df)
        
        s_curve = (row_sums / df.shape[1]).sort_values(ascending=False)
        p_curve = (col_sums / df.shape[0]).sort_values(ascending=True)
        
        # 创建一个 Line 图对象
        line_chart = Line()
        
        # 添加 S 曲线和 P 曲线数据
        line_chart.add_xaxis(xaxis_data=list(s_curve.index))
        line_chart.add_yaxis(series_name="S 曲线 - 学生表现", y_axis=s_curve.values.tolist(), is_smooth=True, linestyle_opts=opts.LineStyleOpts(color="red", width=2, type_="dashed"))
        line_chart.add_yaxis(series_name="P 曲线 - 问题难度", y_axis=p_curve.values.tolist(), is_smooth=True, linestyle_opts=opts.LineStyleOpts(color="blue", width=2))
        
        # 设置图表的全局选项
        line_chart.set_global_opts(title_opts=opts.TitleOpts(title="S-P 曲线图"),
                                   xaxis_opts=opts.AxisOpts(type_="category"),
                                   yaxis_opts=opts.AxisOpts(type_="value", min_=0),
                                   tooltip_opts=opts.TooltipOpts(trigger="axis"))
        
        # 使用 Streamlit ECharts 显示图表
        st_echarts(options=line_chart.dump_options(), height="500px")

        st.write(line_chart.render_embed())
        st.write(s_curve)
        st.write(p_curve)

if __name__ == "__main__":
    main()
