import streamlit as st

st.set_page_config(
    page_title=" Demography Dashboard",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
    )

import pandas as pd
import plotly.express as px
from connection import conn
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
from pyecharts import options as opts
from pyecharts.charts import Pie, Line
from pyecharts.charts import Geo, Liquid
from pyecharts.faker import Faker
from pyecharts.globals import ChartType
from pyecharts.globals import SymbolType
from streamlit_card import card
from streamlit_echarts import st_echarts

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

st.title(':blue[Demography] Of Israel')
st.header('', divider='green')
st.markdown(f"<div style='height: 40px'>", unsafe_allow_html=True) 

#############################
st.write('### Population By Time')   



#df = conn.query('select d.number, t.time, c.category from demography d, time t, category c where d.id_time = t.id_time and d.id_category = c.id_category')
#df = df.sort_values(by='time')
df = pd.read_csv("pop.csv")

# st.write("### Demography Distribution by time")

c = (Bar()
    .add_xaxis([year for year in df['Year']])
    .add_yaxis('Population', [num for num in df['Population']])
    .set_series_opts(
          label_opts=opts.LabelOpts(is_show=False),  # Hide labels by default
      )
)

c.set_global_opts(
        title_opts=opts.TitleOpts(title="", subtitle="Population of Israel "),
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

################## immigration #####################

st.markdown(f"<div style='height: 40px'>", unsafe_allow_html=True) 
st.write('### Immigrants To Israel By Years') 

imigbyyear = pd.read_csv('immg.csv')

imigbyyear['TotalInto'] = pd.to_numeric(imigbyyear['TotalInto'].str.replace(',', ''))

total = imigbyyear['TotalInto'].sum()
st.markdown(f"<div style='border:0.5px solid #e2e2e2; border-radius: 5px; padding: 10px; background-color: #f7f7f7;width:300px;float:right'>"
            f"<p style='color: #333; font-size: 20px; font-weight: bold;'>Total number of Immigrants :</p>"
            f"<p style='color: #0074cc; font-size: 40px;font-weight: bold; text-align: center;'>{total}</p>"
            "</div>", unsafe_allow_html=True)

listpred = [24429, 23874, 23318, 22762, 22206, 21650, 21094, 20538]

num_years_to_predict = st.slider(
    label="Select the number of years to predict:",
    min_value=1,
    max_value=8,
    value=3,  # Default value
    step=1,  # Step size
    key=4
)

listpredicted = [None for i in range(74)]
listpredicted.append(74714)

for i in range(num_years_to_predict):
    listpredicted.append(listpred[i])

date = [i for i in range(1948, 2030)]

c = (Bar()
    .add_xaxis([year for year in date])
    .add_yaxis('Immigrants', [num for num in imigbyyear['TotalInto']])
    .add_yaxis('Immigrants Predicted', listpredicted, color='#0C0')
    .set_series_opts(
          label_opts=opts.LabelOpts(is_show=False),  # Hide labels by default
      )
)

c.set_global_opts(
        title_opts=opts.TitleOpts(title="", subtitle="The numbers of Immigrants"),
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
    graphic_opts=[
            opts.GraphicImage(
                graphic_item=opts.GraphicItem(
                    id_="logo", right=20, top=20, z=-10, bounding="raw", origin=[75, 75]
                ),
                graphic_imagestyle_opts=opts.GraphicImageStyleOpts(
                    image="https://echarts.apache.org/zh/images/favicon.png",
                    width=150,
                    height=150,
                    opacity=0.4,
                ),
            )
        ],
)

st_pyecharts(c)

################## immigration by countries #####################

df2 = pd.read_csv('MigrationToIsrael.csv')
# now we can add the maps of the two things 
fig = px.choropleth(df2, locations="CDE",
                    color="Migrants", # lifeExp is a column of gapminder
                    hover_name="migrant country", # column to add to hover information
                    color_continuous_scale="Viridis",
                    # labels={'log_value': 'number'}
                    )

st.subheader("Immigransts by countries")
st.plotly_chart(fig, theme="streamlit", use_container_width=True)

################## immigration from countries arab #####################
byc = pd.read_csv('IMAr.csv')


types = [t for t in byc['Country']]
nums = [t for t in byc['Immigrants']]

pie = (
        Pie()
        .add(
            "Migrants from Arab Countries",
            [list(z) for z in zip(types, nums)],
            radius=[0, 80],
        )
        .set_global_opts(
            title_opts=opts.TitleOpts("Categories of Prisoners"),
                )
    )

st.subheader("Immigrants From Arab Countries")  
st.markdown(f"<div style='height: 40px'>", unsafe_allow_html=True) 
st_pyecharts(pie)

################## Suisides in Israel #####################

st.markdown(f"<div style='height: 40px'>", unsafe_allow_html=True) 
st.write('### Suisides in Israel by years') 
suic = pd.read_csv('Suicide.csv')

total = suic['Suicides'].sum()
st.markdown(f"<div style='border:0.5px solid #e2e2e2; border-radius: 5px; padding: 10px; background-color: #f7f7f7;width:300px;float:right'>"
            f"<p style='color: #333; font-size: 20px; font-weight: bold;'>Total number of Suicides :</p>"
            f"<p style='color: #0074cc; font-size: 40px;font-weight: bold; text-align: center;'>{total}</p>"
            "</div>", unsafe_allow_html=True)

num_years_to_predict = st.slider(
    label="Select the number of years to predict:",
    min_value=1,
    max_value=7,
    value=3,  # Default value
    step=1  # Step size
)

prd = [461, 465, 470, 475, 479, 484, 488]


listpredicted = [None for i in range(48)]
listpredicted.append(420)

for i in range(num_years_to_predict):
    listpredicted.append(prd[i])

date = [i for i in range(1975, 2030)]

c = (Bar()
    .add_xaxis([year for year in date])
    .add_yaxis('Suicides', [num for num in suic['Suicides']])
    .add_yaxis('Suicides Predicted', listpredicted, color='#0C0')
    .set_series_opts(
          label_opts=opts.LabelOpts(is_show=False),
      )
)

c.set_global_opts(
        title_opts=opts.TitleOpts(title="", subtitle="The numbers of Suicides"),
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


