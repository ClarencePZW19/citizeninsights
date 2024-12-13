import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import plotly.express as px

# Define a color palette with colors close to Google colors
COLOR_PALETTE = [
    '#4285F4', '#44A955', '#E24332', '#F5BE14',
    '#34A853', '#FBBC05', '#EA4335', '#F4B400',
    '#0F9D58', '#F4C20D', '#DB4437', '#F09300',
    '#4285F4', '#34A853', '#EA4335', '#FBBC05',
    '#F4B400', '#0F9D58', '#F4C20D', '#DB4437'
]

def parse_json(data_json):
    """Convert JSON data to a Pandas DataFrame."""
    return pd.json_normalize(data_json)

# Geographic Data Visualizations

def choropleth_map(data_json, geojson):
    data = parse_json(data_json)
    m = folium.Map(location=[0, 0], zoom_start=2)
    folium.Choropleth(
        geo_data=geojson,
        data=data,
        columns=['Region', 'Value'],
        key_on='feature.properties.name',
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Value'
    ).add_to(m)
    st_folium(m, width=700, height=500)

def point_map(data_json):
    data = parse_json(data_json)
    m = folium.Map(location=[0, 0], zoom_start=2)
    for _, row in data.iterrows():
        folium.CircleMarker(
            location=(row.get('lat', 0), row.get('lon', 0)),
            radius=5,
            color='#4285F4',
            fill=True,
            fill_color='#4285F4'
        ).add_to(m)
    st_folium(m, width=700, height=500)

def heat_map(data_json):
    data = parse_json(data_json)
    m = folium.Map(location=[0, 0], zoom_start=2)
    HeatMap(data[['lat', 'lon']].dropna().values).add_to(m)
    st_folium(m, width=700, height=500)

def bubble_map(data_json):
    data = parse_json(data_json)
    m = folium.Map(location=[0, 0], zoom_start=2)
    for _, row in data.iterrows():
        folium.CircleMarker(
            location=(row.get('lat', 0), row.get('lon', 0)),
            radius=row.get('value', 1),
            color='#44A955',
            fill=True,
            fill_color='#44A955'
        ).add_to(m)
    st_folium(m, width=700, height=500)

def flow_map(data_json):
    data = parse_json(data_json)
    m = folium.Map(location=[0, 0], zoom_start=2)
    for _, row in data.iterrows():
        folium.PolyLine(
            locations=[(row.get('start_lat', 0), row.get('start_lon', 0)), 
                       (row.get('end_lat', 0), row.get('end_lon', 0))],
            color='#E24332'
        ).add_to(m)
    st_folium(m, width=700, height=500)

# Numerical or Tabular Data Visualizations

def bar_chart(data_json, x_col='Category', y_col='Value', category_col=None):
    data = parse_json(data_json)
    fig = px.bar(data, x=x_col, y=y_col, color=category_col,
                 color_discrete_sequence=COLOR_PALETTE)
    fig.update_layout(font=dict(family="Roboto Medium"))
    st.plotly_chart(fig, use_container_width=True)

def line_chart(data_json, x_col='Date', y_col='Value', category_col=None):
    data = parse_json(data_json)
    fig = px.line(data, x=x_col, y=y_col, color=category_col,
                  color_discrete_sequence=COLOR_PALETTE)
    fig.update_layout(font=dict(family="Roboto Medium"))
    st.plotly_chart(fig, use_container_width=True)

def scatter_plot(data_json, x_col='X', y_col='Y', category_col=None):
    data = parse_json(data_json)
    fig = px.scatter(data, x=x_col, y=y_col, color=category_col,
                     color_discrete_sequence=COLOR_PALETTE)
    fig.update_layout(font=dict(family="Roboto Medium"))
    st.plotly_chart(fig, use_container_width=True)

def histogram(data_json, x_col='Value', category_col=None):
    data = parse_json(data_json)
    fig = px.histogram(data, x=x_col, color=category_col,
                       color_discrete_sequence=COLOR_PALETTE)
    fig.update_layout(font=dict(family="Roboto Medium"))
    st.plotly_chart(fig, use_container_width=True)

def pie_chart(data_json, names_col='Category', values_col='Value'):
    data = parse_json(data_json)
    fig = px.pie(data, names=names_col, values=values_col,
                 color_discrete_sequence=COLOR_PALETTE)
    fig.update_layout(font=dict(family="Roboto Medium"))
    st.plotly_chart(fig, use_container_width=True)

def box_plot(data_json, x_col='Category', y_col='Value', category_col=None):
    data = parse_json(data_json)
    fig = px.box(data, x=x_col, y=y_col, color=category_col,
                 color_discrete_sequence=COLOR_PALETTE)
    fig.update_layout(font=dict(family="Roboto Medium"))
    st.plotly_chart(fig, use_container_width=True)

def heatmap(data_json):
    data = parse_json(data_json)
    fig = px.imshow(data, color_continuous_scale=COLOR_PALETTE)
    fig.update_layout(font=dict(family="Roboto Medium"))
    st.plotly_chart(fig, use_container_width=True)

def area_chart(data_json, x_col='Date', y_col='Value', category_col=None):
    data = parse_json(data_json)
    fig = px.area(data, x=x_col, y=y_col, color=category_col,
                  color_discrete_sequence=COLOR_PALETTE)
    fig.update_layout(font=dict(family="Roboto Medium"))
    st.plotly_chart(fig, use_container_width=True)

def bubble_chart(data_json, x_col='X', y_col='Y', size_col='Size', category_col=None):
    data = parse_json(data_json)
    fig = px.scatter(data, x=x_col, y=y_col, size=size_col, color=category_col,
                     color_discrete_sequence=COLOR_PALETTE)
    fig.update_layout(font=dict(family="Roboto Medium"))
    st.plotly_chart(fig, use_container_width=True)

def violin_plot(data_json, x_col='Category', y_col='Value', category_col=None):
    data = parse_json(data_json)
    fig = px.violin(data, x=x_col, y=y_col, color=category_col,
                    color_discrete_sequence=COLOR_PALETTE)
    fig.update_layout(font=dict(family="Roboto Medium"))
    st.plotly_chart(fig, use_container_width=True)

# Example usage (uncomment to test with actual JSON data)
# data_json = {...}  # JSON data input
# bar_chart(data_json)