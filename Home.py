#######################
# Import libraries
import streamlit as st
from annotated_text import annotated_text
from streamlit_timeline import timeline
from PIL import Image, ImageDraw, ImageFont
import io
import altair as alt
import pandas as pd
#######################
# Page configuration
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.set_page_config(
    page_title="Palestine vs Israel Dashboard",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
    )


st.image('imgs/img.jpg', caption='', use_column_width=True)
#alt.themes.enable("dark")


st.title('Exploring the Israeli-Palestinian Conflict')
st.write('\n')


# Charger l'image depuis le fichier
# image_path = "imgs/img.jpg"
# image = Image.open(image_path)

# Ajouter du texte à l'image en créant une nouvelle image
# image_with_text = image.copy()
# draw = ImageDraw.Draw(image_with_text)
# font_path = "arial.ttf"  
# font_size = 30
# font = ImageFont.truetype(font_path, font_size)
# text = ' '#Palestine-Israel Conflict'

# draw.text((50,210), text, font=font, fill='#000')

# Afficher l'image modifiée dans Streamlit
# st.image(image_with_text, use_column_width=True)

#st.header(':blue[Israel-Palestine] Conflict A Visual Exploration', divider='green')

# Fonction pour créer un texte encadré avec HTML
def encadrer_texte(texte):
    return f'''<div style='
                font-style: italic;
                font-size: large;
                margin-left: 20px;
                font-family:Arial, Helvetica, sans-serif;
                text-align: justify;
                '>{texte}</div>
            '''


st.write("### Project Overview :")
st.markdown(f"<div style='width: 100%;height: 10px;background-color: #393939;padding-left: 0;z-index: 4;'></div>", unsafe_allow_html=True) 
text = '''This project aims to provide a comprehensive and visually engaging exploration of the Israel-Palestine conflict
through data collection and visualization. Motivated by the need for a nuanced understanding
of this complex geopolitical issue, the project is divided into distinct pages,
each dedicated to visualizing specific aspects such as casualties, settlements, and refugee movements.
The home page serves as a gateway, offering essential context on the conflict's historical background
and current geopolitical landscape. Users can navigate seamlessly through various visualizations,
accompanied by transparent insights into data sources and methodology. By fostering accessibility and clarity, 
this project encourages users to explore and comprehend the multifaceted dimensions of the Israel-Palestine conflict.'''

# Utiliser st.markdown pour afficher le texte encadré
st.markdown(encadrer_texte(text), unsafe_allow_html=True)

st.write('\n')

st.write("### Context of the Conflict :")
st.markdown(f"<div style='width: 100%;height: 10px;background-color: #393939;padding-left: 0;z-index: 4;'></div>", unsafe_allow_html=True) 
text = '''This Gaza war didn’t come out of nowhere,
The Israel-Palestine conflict is a longstanding and deeply rooted geopolitical struggle
that demands attention and understanding. Stemming from historical, religious, and territorial
complexities, the conflict involves the Israeli and Palestinian people and has witnessed a series of events,
negotiations, and disputes. At its core, the struggle revolves around competing claims to the land and the pursuit
of national identity. This context is essential to appreciate the gravity of the data presented in this project, 
shedding light on the human, social, and political dimensions that continue to shape the region. As we delve into
specific aspects through visualizations, a foundational understanding of the conflict's background serves as a 
crucial backdrop for interpreting the data and narratives presented.'''
st.markdown(encadrer_texte(text), unsafe_allow_html=True)
st.write('\n')

st.write("### Data Sources :")
st.markdown(f"<div style='width: 100%;height: 10px;background-color: #393939;padding-left: 0;z-index: 4;'></div>", unsafe_allow_html=True) 
text = 'Here is a list of websites where we found the data.'
st.markdown(encadrer_texte(text), unsafe_allow_html=True)
st.write('\n')
# Données pour le tableau
data = {
    'Name': ['Fatalities','Prisoners', 'Refugees', 'Settlements', 'Israel Dimography'],
    'Dataset': [
        '[statistics.btselem.org](https://statistics.btselem.org/en/all-fatalities/)<br>'
        '[israelpalestinetimeline.org](https://israelpalestinetimeline.org/2023deaths/)<br>'
        '[pcbs.gov.ps](https://www.pcbs.gov.ps/site/lang__en/507/default.aspx)<br>'
        '[ochaopt.org](https://www.ochaopt.org/data/casualties)',

        '[mofa.pna.ps](http://www.mofa.pna.ps/en-us/mediaoffice/ministrynews/administrative-detention)<br>'
        '[btselem.org](https://www.btselem.org/statistics/gaza_detainees_and_prisoners)<br>'
        '[militarycourtwatch.org](https://www.militarycourtwatch.org/page.php?id=J5V0bQevz8a19020AWwFbv7lxv2)<br>'
        '[addameer.org](https://www.addameer.org/statistics)',

        '[unhcr.org](https://www.unhcr.org/refugee-statistics/download/?url=L4zuAR)<br>'
        '[macrotrends.net](https://www.macrotrends.net/countries/PSE/palestinel/refugee-statistics)<br>'
        '[tandfonline.com](https://www.tandfonline.com/doi/full/10.1080/0377919X.2022.2091386)',

        '[www.cbs.gov.il](https://www.cbs.gov.il/en/settlements/Pages/default.aspx?mode=Yeshuv)',

        '[worldometers.info](https://www.worldometers.info/demographics/israel-demographics/)<br>'
        '[data.worldbank.org](https://data.worldbank.org/indicator/SP.POP.TOTL?locations=IL)<br>'
        '[cbs.gov.il](https://www.cbs.gov.il/en/subjects/Pages/Population.aspx)<br>'
        '[countryeconomy.com](https://countryeconomy.com/demography/mortality/causes-death/suicide/israel)<br>'
        '[jewishvirtuallibrary.org](https://www.jewishvirtuallibrary.org/total-immigration-to-israel-by-country-of-origin)<br>'
        '[migrationpolicy.org](https://www.migrationpolicy.org/programs/data-hub/charts/immigrant-and-emigrant-populations-country-origin-and-destination )'
    ]
}

# Créer un DataFrame pandas
df = pd.DataFrame(data)

# Afficher le tableau avec st.markdown
st.markdown(df.to_markdown(), unsafe_allow_html=True)
st.write('\n')
st.write('\n')

st.write("### Methodology:")
st.markdown(f"<div style='width: 100%;height: 10px;background-color: #393939;padding-left: 0;z-index: 4;'></div>", unsafe_allow_html=True) 

st.write('''
        - Data Collection: \n
            After identifying the websites above, we employed various methods for collecting data. Some of 
            the websites provided downloadable data in a variety of formats such as CSV, while others offered 
            APIs for direct access. In cases where neither of these options was available, we utilized web 
            scraping. For scraping, we employed two Python libraries: [Beautiful-Soup](https://beautiful-soup-4.readthedocs.io/en/latest/)
            and [Selenium](https://www.selenium.dev/)
        - Data Cleaning & Analysis: \n
            For the data transoformations we used mainly [Pentaho Data Integration](https://www.hitachivantara.com/en-us/products/pentaho-plus-platform/data-integration-analytics.html) 
            which is a business intelligence (BI) software that provides data integration, OLAP services, data mining and extract, transform, load (ETL) capabilities.
        - Visualization Techniques: \n
            For the visualization we used [Streamlit](https://streamlit.io/) an open-source app framework that lets you create
            web apps from data scripts in pure Python, along with Mysql database that is used to store the data after cleaning.
            The deployment of the project was also handled by [Streamlit Community Cloud](https://share.streamlit.io/).
        \n''')


st.write("### A Breif timeline of events:")
st.markdown(f"<div style='width: 100%;height: 10px;background-color: #393939;padding-left: 0;z-index: 4;'></div>", unsafe_allow_html=True) 


# load data
with open('example.json', "r") as f:
    data = f.read()

# render timeline 600
timeline(data, height=700)






