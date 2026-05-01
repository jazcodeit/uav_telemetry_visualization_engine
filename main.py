import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
import folium

st.title("UAV Telemetry Extraction & Visualization Engine")
st.markdown("Project by [Jaz](https://jazcodeit.ca). View on [GitHub](https://github.com/jazcodeit/uav_telemetry_visualization_engine)")

# read csv file
data = pd.read_csv("demo_data.csv")

# skip if metadata row exist
if "sep=" in data.columns:
    data = pd.read_csv("test.csv", skiprows=1)

## data cleaning start ##

columnsNotToDrop = [
    "CUSTOM.date [local]",
    "CUSTOM.updateTime [local]",
    "OSD.flyTime [s]",
    "OSD.latitude",
    "OSD.longitude",
    "OSD.vpsHeight [ft]",
    "OSD.altitude [ft]",
    "OSD.mileage [ft]",
    "BATTERY.chargeLevel",
    "BATTERY.voltage [V]",
    "OSD.droneType"
]

# drop columns
for column in data:
    if column not in columnsNotToDrop:
        data = data.drop(columns=column)

# remove duplicate rows
data = data.drop_duplicates(["OSD.mileage [ft]"])

# rename columns
data = data.rename(columns={
    "CUSTOM.date [local]": "date",
    "CUSTOM.updateTime [local]": "current_time",
    "OSD.flyTime [s]": "flight_time",
    "OSD.latitude": "latitude",
    "OSD.longitude": "longitude",
    "OSD.vpsHeight [ft]": "agl", # above groud level
    "OSD.altitude [ft]": "altitude",
    "OSD.mileage [ft]": "distance_from_home",
    "BATTERY.chargeLevel": "battery_percent",
    "BATTERY.voltage [V]": "battery_voltage",
    "OSD.droneType": "drone_type"
})

## data cleaning end ##

st.write("Extracted Telemetry Data")
st.write(data) # create dataframe with all of telemetry data

st.header("Battery Information", divider="red")
st.line_chart(data, x='battery_voltage', y='battery_percent', color='battery_percent')


# flight info fields
totalFlightTime = data['flight_time'].max(numeric_only=True)
highestAltitude = data['altitude'].max(numeric_only=True)
highestAGL = data['agl'].max(numeric_only=True)

# get coordinates
homeCoordinates = data[data["distance_from_home"] == data["distance_from_home"].min(numeric_only=True)]
lastLocationCoordinates = data[data["distance_from_home"] == data["distance_from_home"].max(numeric_only=True)]


# Show map with the center distance from home-point and last location
map = folium.Map(
    location=[
        (homeCoordinates["latitude"].item() + lastLocationCoordinates["latitude"].item()) / 2,
        (homeCoordinates["longitude"].item() + lastLocationCoordinates["longitude"].item()) / 2
    ],
    zoom_start=17
)

# add home pinpoint
folium.Marker(
    [homeCoordinates["latitude"].item(), homeCoordinates["longitude"].item()],
    popup="Home-point",
    tooltip="Home-point",
    icon=folium.Icon(color="green", icon="star"),
).add_to(map)

# loop through each coordinates
for latitude, longitude in zip(data["latitude"], data["longitude"]):
    # coordinates from home-point to last location
    pointToPoint = [
        (latitude, longitude),
        (latitude, longitude)
    ]
    # create a trail between home-point and last location
    folium.PolyLine(
        pointToPoint,
        color="blue",
        opacity=0.5,
        weight=10,
    ).add_to(map)

# add last location pinpoint
folium.Marker(
    [lastLocationCoordinates["latitude"].item(), lastLocationCoordinates["longitude"].item()],
    popup="Last Location",
    tooltip="Last Location",
    icon=folium.Icon(color="red", icon="remove"),
).add_to(map)


st.header("Flight Map", divider="red")
st.write(f'Aircraft Model: {data["drone_type"][0]}')
st.write(f'Highest Altitude Reached: {highestAltitude} feet')
st.write(f'Highest AGL Reached: {highestAGL} feet')
st.write(f'Total Flight Time: {round(totalFlightTime / 60)} minutes')
# render map
st_folium(map, width=800)
