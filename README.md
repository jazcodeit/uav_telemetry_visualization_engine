# UAV Telemetry Extraction & Visualization Engine

Extracts and clean telemetry flight data from DJI drone and visualize patterns and trends.

## Demo

[View Demo](https://uav-telemetry-visualization-engine.streamlit.app) and you can checkout more of my projects at [My Website](https://jazcodeit.ca)

## How to use

1. Convert DJI flight data to csv <br/>
[FlightDataConverter](https://www.phantomhelp.com/LogViewer/upload/)

2. Clone this repository <br/>
`git clone https://github.com/jazcodeit/uav_telemetry_visualization_engine.git`

3. Open the terminal and goto **/uav_telemetry_visualization_engine directory** (WINDOWS) <br/>
`cd ./uav_telemetry_visualization_engine`

4. Install the required frameworks and libraries <br/>
`pip install -r requirements.txt`

5. import your flight data in csv format <br/>
`data = pd.read_csv("your_file.csv")`

6. Run streamlit <br/>
`streamlit run yourfile.py`
