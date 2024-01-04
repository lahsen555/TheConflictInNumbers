
import streamlit as st

st.set_page_config(
    page_title=" Settlements Dashboard",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
    )
import pandas as pd
import plotly.express as px
from connection import conn


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

st.title('Israeli :blue[Settlements] In The West Bank')
st.header('', divider='green')

############ population #############


st.markdown(f"<div style='height: 40px'>", unsafe_allow_html=True) 
st.write('### Settlements by Population')

df = conn.query('SELECT s.settlement, ns.Number from settlement s, number_israeli_settlement ns where s.id_settlement = ns.id_settlement')
df = df.groupby('settlement', as_index=False).sum()
df = df.sort_values(by='Number', ascending=False)

top_n = st.number_input(" Choose number of settlements:", min_value=0, max_value=df['settlement'].count(), value=5)

tab1, tab2= st.tabs(["pie", "bar Chart"])
top_elements = df.head(top_n)
    
rest_elements = pd.DataFrame({'settlement': ['Other'], 'Number': [df['Number'][top_n:].sum()]})

# Concatenate the top elements and the 'Other' row
modified_data = pd.concat([top_elements, rest_elements])

# Create the pie chart
fig = px.pie(modified_data, names='settlement', values='Number', title='Top Most Settlements By Population')
modified_data = modified_data.rename(columns={'Number': 'populations'})

with tab2:
    st.markdown(f"<div style='height: 20px'>", unsafe_allow_html=True) 
    st.bar_chart(modified_data, x='settlement', y='populations',height=400)
with tab1:
    st.plotly_chart(fig, use_container_width=True)

total = total =df['Number'].sum()
st.markdown(f"<div style='border:0.5px solid #e2e2e2; border-radius: 5px; padding: 10px; background-color: #f7f7f7;width:300px;float:right'>"
            f"<p style='color: #333; font-size: 20px; font-weight: bold;'>Total number of settlers :</p>"
            f"<p style='color: #0074cc; font-size: 40px;font-weight: bold; text-align: center;'>{total}</p>"
            "</div>", unsafe_allow_html=True)


if st.checkbox("Dataset population"):
    st.dataframe(df)


########## Maps ###############

dfmap = conn.query('select s.settlement, s.X as lat, s.Y as lon, ns.number from settlement s, number_israeli_settlement ns where s.id_settlement = ns.id_settlement')

agg_func = {'lon': 'first', 'lat': 'first', 'number': 'sum'}

dfmap = dfmap.groupby('settlement', as_index=False).agg(agg_func)

dfmap['lon'] = dfmap['lon'].astype(float)
dfmap['lat'] = dfmap['lat'].astype(float)

fig = px.scatter_mapbox(dfmap,
                    lat='lat', 
                    lon='lon',
                    size="number",
                    zoom=7,
                    mapbox_style='open-street-map',
                    width=1100,
                    height=600,
                    hover_name="settlement")

st.plotly_chart(fig)

if st.checkbox("Dataset maps"):
    st.dataframe(dfmap)

########### Establishment ##############

st.markdown(f"<div style='height: 40px'>", unsafe_allow_html=True) 
st.write('### Number of settlements established')


dfEstablished = conn.query('select count(DISTINCT s.settlement) as count, s.Established from settlement s, number_israeli_settlement ns where s.id_settlement = ns.id_settlement group by s.Established')
df = dfEstablished.sort_values(by='Established', ascending=False)
total = df['count'].sum()

df=df[df['Established'] != 0]


st.markdown(f"<div style='height: 10px'>", unsafe_allow_html=True) 


st.markdown(f"<div style='border:0.5px solid #e2e2e2; border-radius: 5px; padding: 10px; background-color: #f7f7f7;width:300px;float:right'>"
            f"<p style='color: #333; font-size: 20px; font-weight: bold;'>Total number of Settlements:</p>"
            f"<p style='color: #0074cc; font-size: 40px;font-weight: bold; text-align: center;'>{total}</p>"
            "</div>", unsafe_allow_html=True)

df = df.rename(columns={'count': 'Number of settlement'})
df = df.rename(columns={'Established': 'Establishment'})


st.bar_chart(df, x='Establishment', y='Number of settlement')


if st.checkbox("Dataset establishment"):
    st.dataframe(df)
