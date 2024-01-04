import streamlit as st

st.set_page_config(
    page_title=" Prisoners Dashboard",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
    )
import pandas as pd
from connection import conn
import plotly.express as px
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts, st_echarts




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

st.title('Palestinian :blue[Prisoners] And :blue[Detainees] In Israel')
st.header('', divider='green')

############## import data ##################

df = conn.query('''select p.number, pt.type, t.time 
                from prisoners p, prisoners_type pt, time t 
                where p.id_prisoners_type = pt.id_prisoners_type and p.id_time = t.id_time''', ttl=600)

#############Prisoners by time ##############

st.markdown(f"<div style='height: 40px'>", unsafe_allow_html=True) 
st.write('### Prisoners by time')
Prisoners_time = df
###choose time
choix = Prisoners_time['type'].unique().tolist()
choix.insert(0, 'All')
choix = pd.Series(choix)
selectionnee = st.selectbox("choose the type :", choix)
if selectionnee != 'All':
    Prisoners_time = Prisoners_time[Prisoners_time['type'] == selectionnee]
Prisoners_time = Prisoners_time.drop(columns='type')
Prisoners_time.rename(columns={'number': 'number of prisoners'}, inplace=True)
Prisoners_time = Prisoners_time.groupby(['time'], as_index=False).sum()

chart = (Bar()
    .add_xaxis([year for year in Prisoners_time['time']])
    .add_yaxis('2001-2023 Prisoners by (numbers)', [num for num in Prisoners_time['number of prisoners']])
    .set_global_opts(title_opts=opts.TitleOpts(title="Prisoners Over Time", subtitle="2001-2023 Prisoners"),
                     toolbox_opts=opts.ToolboxOpts())
    .set_series_opts(
          label_opts=opts.LabelOpts(is_show=False)# Hide labels by default
      )                 
                     
)

chart.set_global_opts(
        title_opts=opts.TitleOpts(title="", subtitle="The numbers of prisoners"),
        toolbox_opts=opts.ToolboxOpts(
             feature=opts.ToolBoxFeatureOpts(
                 save_as_image=opts.ToolBoxFeatureSaveAsImageOpts(title="Download as Image"),
                 restore=opts.ToolBoxFeatureRestoreOpts(title="Restore"),
                 data_view=opts.ToolBoxFeatureDataViewOpts(title="View Data", lang=["Data View", "Close", "Refresh"]),
                 data_zoom=opts.ToolBoxFeatureDataZoomOpts(zoom_title="Zoom In",back_title="Zoom Out"),
                 magic_type=opts.ToolBoxFeatureMagicTypeOpts(line_title="Line Chrat", bar_title="Somethinf", stack_title="Stack"),
        )),
    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="none"),
    xaxis_opts=opts.AxisOpts(
              axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(opacity=0)),
              splitline_opts=opts.SplitLineOpts(is_show=False), 
              splitarea_opts=opts.SplitAreaOpts(is_show=False)   # Hide grid areas
          ),
)
st_pyecharts(chart,height=500)

total = df['number'].sum()
st.markdown(f"<div style='border:0.5px solid #e2e2e2; border-radius: 5px; padding: 10px; background-color: #f7f7f7;width:300px;float:right'>"
            f"<p style='color: #333; font-size: 20px; font-weight: bold;'>Total number of Prisoners :</p>"
            f"<p style='color: #0074cc; font-size: 40px;font-weight: bold; text-align: center;'>{total}</p>"
            "</div>", unsafe_allow_html=True)




############# Prisoners by type ##############

# st.markdown(f"<div style='height: 40px'>", unsafe_allow_html=True) 
# st.write('### Prisoners by type')    

# prisoners_type = df

# ###choose time
# choix = prisoners_type['time'].unique().tolist()
# choix.insert(0, 'All')
# choix = pd.Series(choix)
# selectionnee = st.selectbox("choose the year :", choix)
# if selectionnee != 'All':
#     prisoners_type = prisoners_type[prisoners_type['time'] == selectionnee]
# prisoners_type = prisoners_type.drop(columns='time')
# prisoners_type = prisoners_type.groupby(['type'], as_index=False).sum()

# fig = px.pie(prisoners_type, values='number', names='type', title=f'Type of Prisoners')

# st.plotly_chart(fig, theme=None, use_container_width=True)

    
# if st.checkbox('dataset by type'):
#     st.dataframe(prisoners_type)



# prisoners_tyep = conn.query('select p.number, pt.type from prisoners p, prisoners_type pt where p.id_prisoners_type = pt.id_prisoners_type')

# prisoners_tyep = prisoners_tyep.groupby('type', as_index=False).sum()

# st.write("#### Prisoners By Type")
# selected_year = st.slider('Select a year', 2010, 2023, 2012)
    
# option = {
#     "legend": {},
#     "tooltip": {"trigger": "axis", "showContent": False},
#     "dataset": {
#         "source": [
#             ["type","2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"],
#             [prisoners_tyep['type'][0], 204, 307, 178, 150, 463, 584, 535, 437, 494, 464, 376, 495, 784, 1310],
#             [prisoners_tyep['type'][1], 683, 625, 1031, 1351, 1511, 1740, 1594, 1763, 1429, 1027, 990, 1007, 1090, 1117],
#             [prisoners_tyep['type'][2], 153, 152, 219, 189, 206, 297, 253, 318, 240, 197, 159, 103, 105, 115],
#             [prisoners_tyep['type'][3], 4662, 3196,3089, 3078, 3347, 3445, 3561, 3458, 3207, 2855, 2634, 2413, 2262, 2222],
#         ]
#     },
#     "xAxis": {"type": "category"},
#     "yAxis": {"gridIndex": 0},
#     "grid": {"top": "50%"},
#     "series": [
#         {
#             "type": "line",
#             "smooth": True,
#             "seriesLayoutBy": "row",
#             "emphasis": {"focus": "series"},
#         },
#         {
#             "type": "line",
#             "smooth": True,
#             "seriesLayoutBy": "row",
#             "emphasis": {"focus": "series"},
#         },
#         {
#             "type": "line",
#             "smooth": True,
#             "seriesLayoutBy": "row",
#             "emphasis": {"focus": "series"},
#         },
#         {
#             "type": "line",
#             "smooth": True,
#             "seriesLayoutBy": "row",
#             "emphasis": {"focus": "series"},
#         },
#         {
#             "type": "pie",
#             "id": "pie",
#             "radius": "30%",
#             "center": ["50%", "25%"],
#             "emphasis": {"focus": "data"},
#             "label": {"formatter": "{b}: {@2012} ({d}%)"},
#             "encode": {"itemName": "type", "value": f"{selected_year}", "tooltip": f"{selected_year}"},
#         },
#     ],
# }

# st_echarts(option, height="500px", key="echarts")


###########################
st.write("#### Prisoners By Type")
selected_year = st.slider('Select a year', 2001, 2023, 2012)

# prisoners_tyep = conn.query('select p.number, pt.type, t.time from prisoners p, prisoners_type pt, time t where p.id_prisoners_type = pt.id_prisoners_type and p.id_time = t.id_time')
types = conn.query("select type from prisoners_type")

years = ["type"] 
for i in range(2001, 2024):
    years.append(str(i))
    
source = [years]

requete = conn.query(f"""
                SELECT p.number , pt.type, t.time
                FROM prisoners p, prisoners_type pt, time t
                WHERE p.id_prisoners_type = pt.id_prisoners_type
                    AND p.id_time = t.id_time
            """)

for j in range(4):
    typepris = [types.iloc[j, 0]]
    for i in range(2001, 2024):
        prisoners_tyep = requete.loc[(requete['time'] == i) & (requete['type'] == types.iloc[j, 0])]['number']
        prisoners_tyep_list = prisoners_tyep.values.tolist()
        typepris.append(prisoners_tyep_list[0])
    source.append(typepris)
    
option = {
    "legend": {},
    "tooltip": {"trigger": "axis", "showContent": False},
    "dataset": {
        "source": [*source]
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