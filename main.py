import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
import folium

# read csv file
data = pd.read_csv('FlightRecord_2026-04-23_11-43-12.csv')

# get coordinates
homeCoordinates = data[data["distance_to_home_m"] == data["distance_to_home_m"].min(numeric_only=True)]
lastLocationCoordinates = data[data["distance_to_home_m"] == data["distance_to_home_m"].max(numeric_only=True)]

# Streamlit Webpage
st.title("UAV Telemetry Extraction & Visualization Engine")
st.write("Extracted Telemetry Data")
st.write(data) # create dataframe with all of telemetry data

# Show map with the center distance from homepoint and last location
map = folium.Map(
    location=[
        50.57171868,
        -111.8892683
    ],
    zoom_start=17
)

# add home pinpoint
folium.Marker(
    [homeCoordinates["lat"].item(), homeCoordinates["lng"].item()],
    popup="Homepoint",
    tooltip="Homepoint",
    icon=folium.Icon(color="green", icon="star"),
).add_to(map)

# coordinates homepoint to last location
pointToPoint = [
    (homeCoordinates["lat"].item(), homeCoordinates["lng"].item()),
    (lastLocationCoordinates["lat"].item(), lastLocationCoordinates["lng"].item())
]

# create a trail between homepoint and last location
folium.PolyLine(
    pointToPoint,
    color="blue",
    opacity=0.5,
    weight=10,

).add_to(map)

# add last location pinpoint
folium.Marker(
    [lastLocationCoordinates["lat"].item(), lastLocationCoordinates["lng"].item()],
    popup="Last Location",
    tooltip="Last Location",
    icon=folium.Icon(color="red", icon="remove"),
).add_to(map)

# render map
st_folium(map, width=800)