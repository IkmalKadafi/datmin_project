import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
from millify import millify
from PIL import Image

# Image path
image = Image.open('Data/choropleth.png')
st.set_page_config(
    page_title="IPM Indonesia 2023 Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded")

# Title 
st.title("Dashboard IPM Indonesia 2023")

# Load Data
def load_df1():
    df1 = pd.read_csv("Data/df_clean.csv")

    df1.drop(df1.columns[df1.columns.str.contains(
        'unnamed', case=False)], axis=1, inplace=True)
    return df1

df1 = load_df1()

def load_df2():
    df2 = pd.read_csv("Data/data_ipm.csv")

    df2.drop(df2.columns[df2.columns.str.contains(
        'unnamed', case=False)], axis=1, inplace=True)
    return df2
df2 = load_df2()

def load_df3():
    df3 = pd.read_csv("Data/data_geomap.csv")
    df3.drop(df3.columns[df3.columns.str.contains(
        'unnamed', case=False)], axis=1, inplace=True)
    return df3
df3 = load_df3()

# Pie Chart
def pie_chart():
    # Extract the values and labels from the data
    values = list(df2['IPM Class'].value_counts())
    labels = df2['IPM Class'].unique().tolist()

    # Define the custom order
    custom_order = ['tinggi', 'sedang', 'sangat tinggi', 'rendah']

    # Sort the labels according to the custom order
    sorted_labels = sorted(labels, key=lambda x: custom_order.index(x))

    # Create the pie chart
    fig = go.Figure(data=[go.Pie(labels=sorted_labels, values=values)])

    # Customize the chart
    fig.update_layout(
        title='IPM Class Distribution',
        legend_title='IPM Class',
        font_size=16
    )
    # Display the chart
    return fig

# Choropleth Map
def choropleth_map():
    # Assign GeoJSON data and other properties
    fig = px.choropleth(df3, geojson=df3.geometry, locations=df3.name,
                        color='IPM', height=500, color_continuous_scale='rdylgn', 
                        hover_name='name', hover_data=None)

# Perform a property update operation on all geo objects that satisfy the specified selection criteria
    fig.update_geos(fitbounds='locations', visible=True)

# Update the layout
    fig.update_layout(title_text='Indonesia IPM Based on Regencies 2023')
    fig.update(layout = dict(title=dict(x=0.46)))
    fig.update_layout(margin={'r':0,'t':30,'l':10,'b':10}, coloraxis_colorbar={'title':'IPM'})

# Generate the map
    return fig

# Define The layout
col = st.columns((1.5, 4.5, 2), gap='medium')
# creates the container for page title
with col[0]:
    st.markdown("### Rata-rata variabel")
    st.write("")

    total_uhh = df1['UHH (tahun)'].mean()
    col[0].metric(label="Umur Harapan Hidup", value=millify(total_uhh, precision=2))

    total_hls = df1['HLS (tahun)'].mean()
    col[0].metric(label="Harapan Lama Sekolah", value=millify(total_hls, precision=2))

    total_rls = df1['RLS (tahun)'].mean()
    col[0].metric(label="Rata-rata Lama Sekolah", value=millify(total_rls, precision=2))

    

with col[1]:    
    pie = pie_chart()
    st.plotly_chart(pie, use_container_width=True)



with col[2]:
    st.markdown('#### IPM per Daerah')

    st.dataframe(df1,
                 column_order=("Daerah", "IPM"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "Daerah": st.column_config.TextColumn(
                        "Daerah",
                    ),
                    "IPM": st.column_config.ProgressColumn(
                        "IPM",
                        format="%f",
                        min_value=0,
                        max_value=max(df1.IPM),
                     )}
                 )
    
col1 = st.columns((5,5), gap='medium')
with col1[0]:
    st.image(image)

with col1[1]:
    st.write(df2)
