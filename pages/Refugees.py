import streamlit as st

st.set_page_config(
    page_title=" Refugees Dashboard",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
    )
import plotly.express as px
from connection import conn
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie
from streamlit_echarts import st_pyecharts
import pandas as pd

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

st.title('Palestinian :blue[Refugees] In The World')
st.header('', divider='green')

########### refugge by time ############


st.markdown(f"<div style='height: 40px'>", unsafe_allow_html=True) 
st.write('### Refugees by time')

df = conn.query('SELECT r.number, t.time from refugee r, time t where r.id_time = t.id_time')
df = df.groupby(['time'], as_index=False).sum()


total = total =df['number'].sum()
st.markdown(f"<div style='border:0.5px solid #e2e2e2; border-radius: 5px; padding: 10px; background-color: #f7f7f7;width:300px;float:right'>"
            f"<p style='color: #333; font-size: 20px; font-weight: bold;'>Total number of refugees :</p>"
            f"<p style='color: #0074cc; font-size: 40px;font-weight: bold; text-align: center;'>{total}</p>"
            "</div>", unsafe_allow_html=True)



chart = (Bar()
    .add_xaxis([year for year in df['time']])
    .add_yaxis('2001-2023 Refugees by (numbers)', [num for num in df['number']])
    .set_series_opts(
          label_opts=opts.LabelOpts(is_show=False),  # Hide labels by default
      )
)

chart.set_global_opts(
    title_opts=opts.TitleOpts(title="", subtitle="Total number of Refugees between 2001-2023"),
    toolbox_opts=opts.ToolboxOpts(
        feature=opts.ToolBoxFeatureOpts(
            save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(title="Download as Image"),
            restore=opts.ToolBoxFeatureRestoreOpts(title="Restore"),
            data_view=opts.ToolBoxFeatureDataViewOpts(title="View Data", lang=["Data View", "Close", "Refresh"]),
            data_zoom=opts.ToolBoxFeatureDataZoomOpts(zoom_title="Zoom In", back_title="Zoom Out"),
            magic_type=opts.ToolBoxFeatureMagicTypeOpts(line_title="Line Chart", bar_title="Something", stack_title="Stack"),
        )
    )
)
st_pyecharts(chart,height=500)


##### refugee by category #############

st.markdown(f"<div style='height: 40px'>", unsafe_allow_html=True) 
st.write('### Refugees by categories')

df1 = conn.query('select d.number, c.category from refugee d, category c where d.id_category = c.id_category')
df1 = df1.groupby(['category'], as_index=False).sum()
df1['category'] = df1['category'].replace({'C': 'child'})
df1['category'] = df1['category'].replace({'F': 'female'})
df1['category'] = df1['category'].replace({'M': 'male'})

pie = (
        Pie()
        .add(
            "Categories of refugees",
            [list(z) for z in zip(df1['category'], df1['number'])],
        )
        .set_global_opts(title_opts=opts.TitleOpts("Categories of refugees"))
    )
#st_pyecharts(pie)
 

st.markdown(f"<div style='height: 20px'>", unsafe_allow_html=True) 
st_pyecharts(pie)

if st.checkbox('dataset category'):
    st.dataframe(df1)


################ refugee by country ################# 

st.markdown(f"<div style='height: 40px'>", unsafe_allow_html=True) 
st.write('### Refugees by asylum country')

df2 = conn.query('select d.number, c.country_code, c.country from refugee d, country c where d.id_country = c.id_country')

df2 = df2.groupby(['country','country_code'], as_index=False).sum()
df2 = df2.sort_values(by='number', ascending=False)
top_n = 10
df3 = df2.drop(columns='country_code')
top_elements = df3.head(top_n)
rest_elements = pd.DataFrame({'country': ['Other'], 'number': [df3['number'][top_n:].sum()]})
# Concatenate the top elements and the 'Other' row
modified_data = pd.concat([top_elements, rest_elements])
# Create the pie chart
fig = px.pie(modified_data, names='country', values='number', title='Top 10 countries with the most asylum seekers')    

tab1, tab2= st.tabs(["pie", "Map"])

fig1 = px.choropleth(df2, locations="country_code",
                    color="number", # lifeExp is a column of gapminder
                    hover_name="country", # column to add to hover information
                    labels={'number': 'number'},
                    width=800,
                    height=600
                    )

with tab1:
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
with tab2:
    st.plotly_chart(fig1, use_container_width=True)    
    
if st.checkbox('dataset asylum country'):
    st.dataframe(df2)