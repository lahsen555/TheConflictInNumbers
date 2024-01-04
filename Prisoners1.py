import streamlit as st
import pandas as pd
from connection import conn
import plotly.express as px
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from streamlit_echarts import st_pyecharts, st_echarts



st.header('This is the :blue[Prisoners] page', divider='green')

df = conn.query('select p.number, t.time from prisoners p, time t where p.id_time = t.id_time')

df.rename(columns={'number': 'number of prisoners'}, inplace=True)

prisoners_tyep = conn.query('select p.number, pt.type from prisoners p, prisoners_type pt where p.id_prisoners_type = pt.id_prisoners_type')

fig = px.pie(prisoners_tyep, values='number', names='type', title=f'Categories of Prisoners')

prisoners_tyep = prisoners_tyep.groupby('type', as_index=False).sum()

types = [t for t in prisoners_tyep['type']]
nums = [t for t in prisoners_tyep['number']]

prisoners_over_time = df.groupby(['time'], as_index=False).sum()

c = (Bar()
    .add_xaxis([year for year in prisoners_over_time['time']])
    .add_yaxis('Prisoners', [num for num in prisoners_over_time['number of prisoners']])
    .set_series_opts(
          label_opts=opts.LabelOpts(is_show=False),  # Hide labels by default
      )
)

c.set_global_opts(
        title_opts=opts.TitleOpts(title="Prisoners By Time", subtitle="The numbers of Prisoners btween 2000 and 2023"),
        toolbox_opts=opts.ToolboxOpts(
            feature=opts.ToolBoxFeatureOpts(
                save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(title="Download as Image"),
                restore=opts.ToolBoxFeatureRestoreOpts(title="Restore"),
                data_view=opts.ToolBoxFeatureDataViewOpts(title="View Data", lang=["Data View", "Close", "Refresh"]),
                data_zoom=opts.ToolBoxFeatureDataZoomOpts(zoom_title="Zoom In",back_title="Zoom Out"),
                magic_type=opts.ToolBoxFeatureMagicTypeOpts(line_title="Line Chrat", bar_title="Somethinf", stack_title="Stack"),
        )
    ),
    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="none"),
    xaxis_opts=opts.AxisOpts(
              axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(opacity=0)),
              splitline_opts=opts.SplitLineOpts(is_show=False), 
              splitarea_opts=opts.SplitAreaOpts(is_show=False)   # Hide grid areas
          ),
)


st_pyecharts(c)
    
st.write("#### Prisoners By Type")
selected_year = st.slider('Select a year', 2010, 2023, 2012)
    
option = {
    "legend": {},
    "tooltip": {"trigger": "axis", "showContent": False},
    "dataset": {
        "source": [
            ["type","2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"],
            [prisoners_tyep['type'][0], 204, 307, 178, 150, 463, 584, 535, 437, 494, 464, 376, 495, 784, 1310],
            [prisoners_tyep['type'][1], 683, 625, 1031, 1351, 1511, 1740, 1594, 1763, 1429, 1027, 990, 1007, 1090, 1117],
            [prisoners_tyep['type'][2], 153, 152, 219, 189, 206, 297, 253, 318, 240, 197, 159, 103, 105, 115],
            [prisoners_tyep['type'][3], 4662, 3196,3089, 3078, 3347, 3445, 3561, 3458, 3207, 2855, 2634, 2413, 2262, 2222],
        ]
    },
    "xAxis": {"type": "category"},
    "yAxis": {"gridIndex": 0},
    "grid": {"top": "55%"},
    "series": [
        {
            "type": "line",
            "smooth": True,
            "seriesLayoutBy": "row",
            "emphasis": {"focus": "series"},
        },
        {
            "type": "line",
            "smooth": True,
            "seriesLayoutBy": "row",
            "emphasis": {"focus": "series"},
        },
        {
            "type": "line",
            "smooth": True,
            "seriesLayoutBy": "row",
            "emphasis": {"focus": "series"},
        },
        {
            "type": "line",
            "smooth": True,
            "seriesLayoutBy": "row",
            "emphasis": {"focus": "series"},
        },
        {
            "type": "pie",
            "id": "pie",
            "radius": "30%",
            "center": ["50%", "25%"],
            "emphasis": {"focus": "data"},
            "label": {"formatter": "{b}: {@2012} ({d}%)"},
            "encode": {"itemName": "type", "value": f"{selected_year}", "tooltip": f"{selected_year}"},
        },
    ],
}

st_echarts(option, height="500px", key="echarts")