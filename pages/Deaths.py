import streamlit as st

st.set_page_config(
    page_title=" Deaths Dashboard",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
    )

import pandas as pd
import plotly.express as px
from connection import conn
from pyecharts.charts import Bar, Pie
from streamlit_echarts import st_pyecharts
from pyecharts import options as opts
from pyecharts.charts import Liquid
from pyecharts.globals import SymbolType



st.markdown(
    """
    <style>
        .title {
            text-align: center;
            font-size: 2.5em;
            color: #3366cc;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('War-Related :red[Deaths] In Israel And Palestine')
st.header('', divider='green')

############# deaths by time ################
st.markdown(f"<div style='height: 40px'>", unsafe_allow_html=True) 

dfist = conn.query('SELECT count(id_death) as sizei, t.time from death d, time t where d.id_time = t.id_time and d.id_country = 1 group by t.time;',ttl=600)
dfpalt = conn.query('SELECT count(id_death) as sizep, t.time from death d, time t where d.id_time = t.id_time and d.id_country = 2 group by t.time;',ttl=600)
### total
total = dfist['sizei'].sum() + dfpalt['sizep'].sum()
st.markdown(f"<div style='border:0.5px solid #e2e2e2; border-radius: 5px; padding: 10px; background-color: #f7f7f7;width:300px;float:right'>"
            f"<p style='color: #333; font-size: 20px; font-weight: bold;'>Total number of Deaths :</p>"
            f"<p style='color: #0074cc; font-size: 40px;font-weight: bold; text-align: center;'>{total}</p>"
            "</div>", unsafe_allow_html=True)

liste = pd.merge(dfist, dfpalt,on='time', how='outer')
liste =liste.fillna(0)
liste =liste.sort_values(by='time')

ct = (Bar()
    .add_xaxis([(f"{year}") for year in liste['time']])
    .add_yaxis('Israel', [num for num in liste['sizei']])
    .add_yaxis('Palestine', [num for num in liste['sizep']])
    .set_series_opts(
          label_opts=opts.LabelOpts(is_show=False)# Hide labels by default
      )
)

ct.set_global_opts(
        title_opts=opts.TitleOpts(title="", subtitle="Number of Deaths"),
        toolbox_opts=opts.ToolboxOpts(
            feature=opts.ToolBoxFeatureOpts(
                save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(title="Download as Image"),
                restore=opts.ToolBoxFeatureRestoreOpts(title="Restore"),
                data_view=opts.ToolBoxFeatureDataViewOpts(title="View Data", lang=["Data View", "Close", "Refresh"]),
                data_zoom=opts.ToolBoxFeatureDataZoomOpts(zoom_title="Zoom In",back_title="Zoom Out"),
                magic_type=opts.ToolBoxFeatureMagicTypeOpts(line_title="Line Chrat", bar_title="Somethinf", stack_title="Stack")
        )
    ),
    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="none"),
    xaxis_opts=opts.AxisOpts(
              axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(opacity=0)),
              splitline_opts=opts.SplitLineOpts(is_show=False), 
              splitarea_opts=opts.SplitAreaOpts(is_show=False)   # Hide grid areas
          )
)

st.write('### Death by years')
st_pyecharts(ct) 




############# deaths by age ################
st.markdown(f"<div style='height: 40px'>", unsafe_allow_html=True) 
st.write('### Deaths by age')

dfis = conn.query('SELECT count(id_death) as sizei, Age from death where id_country = 1 group by age;',ttl=600)
dfpal= conn.query('SELECT count(id_death) as sizep, Age from death where id_country = 2 group by age;',ttl=600)

list2 = pd.merge(dfis, dfpal,on='Age', how='outer')
list2 =list2.fillna(0)
list2 =list2.sort_values(by='Age')

ca = (Bar()
    .add_xaxis([(f"{year}") for year in list2['Age']])
    .add_yaxis('Israel', [num for num in list2['sizei']])
    .add_yaxis('Palestine', [num for num in list2['sizep']])
    .set_series_opts(
          label_opts=opts.LabelOpts(is_show=False),  # Hide labels by default
      )
)

ca.set_global_opts(
        title_opts=opts.TitleOpts(title="", subtitle="Number of Deaths"),
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

st_pyecharts(ca)


st.markdown(f"<div style='height: 40px'>", unsafe_allow_html=True) 

#################### death by category  #################### 
st.markdown(f"<div style='height: 40px'>", unsafe_allow_html=True) 
st.write('### Deaths by gender')

df1 = conn.query('''SELECT id_death, c.Category, t.time 
                 from death d, category c, time t 
                 where d.id_category = c.id_category and d.id_time = t.id_time;''', ttl=600)

dfmale = df1[df1['Category']=='M'].drop(columns='Category')
dffemale = df1[df1['Category']=='F'].drop(columns='Category')

dfmale = dfmale.groupby('time',as_index=False).count()
dffemale = dffemale.groupby('time',as_index=False).count()

liste = pd.merge(dfmale, dffemale, on='time', how='outer')
liste =liste.fillna(0)
liste =liste.sort_values(by='time')
#fig1 = px.pie(df1, values='size', names='Category')

bar = (Bar()) 

bar.add_xaxis([year for year in liste['time']])
bar.add_yaxis("M", [num for num in liste['id_death_x']])
bar.add_yaxis("F", [num for num in liste['id_death_y']])
bar.set_series_opts(
          label_opts=opts.LabelOpts(is_show=False),  # Hide labels by default
      )

bar.set_global_opts(
        title_opts=opts.TitleOpts(title="", subtitle="Numbers of deaths"),
        toolbox_opts=opts.ToolboxOpts(
            feature=opts.ToolBoxFeatureOpts(
                save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(title="Download as Image"),
                restore=opts.ToolBoxFeatureRestoreOpts(title="Restore"),
                data_view=opts.ToolBoxFeatureDataViewOpts(title="View Data", lang=["Data View", "Close", "Refresh"]),
                data_zoom=opts.ToolBoxFeatureDataZoomOpts(zoom_title="Zoom In",back_title="Zoom Out"),
                magic_type=opts.ToolBoxFeatureMagicTypeOpts(line_title="Line Chrat", bar_title="Somethinf", stack_title="Stack"), 
        ),
    ),
    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="none"),
    xaxis_opts=opts.AxisOpts(
              axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(opacity=0)),
              splitline_opts=opts.SplitLineOpts(is_show=False), 
              splitarea_opts=opts.SplitAreaOpts(is_show=False)   # Hide grid areas
          ),
)

st_pyecharts(bar)



#################### death by type of injury  #################### 
st.markdown(f"<div style='height: 40px'>", unsafe_allow_html=True) 
st.write('### Deaths by type of injury')

df2 = conn.query('SELECT count(d.id_death) as count_type, n.type_of_injury from death d, type_of_injury n where d.id_injury = n.id_injury group by type_of_injury;', ttl=600)
df2 = df2.sort_values(by='count_type', ascending=False)

top_n = 5

#Extract the top N elements
top_elements = df2.head(top_n)
rest_elements = pd.DataFrame({'type_of_injury': ['Other'], 'count_type': [df2['count_type'][top_n:].sum()]})
# Concatenate the top elements and the 'Other' row
modified_data = pd.concat([top_elements, rest_elements])
modified_data = modified_data.replace({'type_of_injury': {'N': 'Anonyme'}})

pie = (
        Pie()
        .add(
            "type",
            [list(z) for z in zip(modified_data['type_of_injury'], modified_data['count_type'])],
        )
        .set_global_opts(title_opts=opts.TitleOpts(""))
    )

st.markdown(f"<div style='height: 40px'>", unsafe_allow_html=True) 
st_pyecharts(pie,height=500)

if st.checkbox('dataset by type of injury'):
    st.dataframe(df2)

