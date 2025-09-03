 # velociCity
Unlock the hidden patterns of urban movement — from rush-hour bottlenecks to accident-prone streets

   velociCity   is an interactive web application that identifies congestion patterns, accident-prone areas, and peak traffic hours using GPS/traffic datasets. Unlike routine traffic apps, this tool provides   data-driven insights   into urban mobility, helping planners, commuters, and researchers understand city movement dynamics.

---

   🔹 Key Features

-   Hotspot Detection  : Identify high-density traffic areas and accident-prone locations using spatial clustering (DBSCAN).  
-   Interactive Map Visualization  : Explore traffic patterns with Folium maps and heatmaps.  
-   Time-of-Day & Weekday Analysis  : Discover peak traffic hours and patterns by weekdays.  
-   Hotspot Summary Export  : Export detected clusters with severity scores for further analysis.  
-   User-Friendly Upload  : Upload your own CSV dataset or use the provided sample.  
-   Customizable Clustering  : Adjust DBSCAN parameters (radius and minimum points) via the web interface for sensitivity tuning.  

---

    Demo

You can preview the app locally or deploy it on   Streamlit Cloud / Render / Docker  .

- Example screenshot of hotspot map and charts (add your own screenshots here in future updates).  

---

   🔹 Tech Stack

-   Python 3.10+  
-   Streamlit   — for interactive web UI
-   Pandas & NumPy   — data processing
-   scikit-learn   — DBSCAN clustering
-   Folium & streamlit-folium   — mapping and heatmaps
-   Plotly   — interactive charts
-   Geopy   — optional for geocoding / street names

---

   🔹 Dataset

For demonstration, the project includes a   sample dataset  :

-   File:   `data/sample_traffic.csv`
-   Columns:    
  - `latitude` (float)  
  - `longitude` (float)  
  - `timestamp` (ISO datetime string, e.g., 2023-09-01 08:05:00)  
  - `speed` (optional, km/h)  
  - `incident` (optional, 0 or 1)  

-   Source of sample data:    
  The sample data was   synthetically generated   to simulate real GPS traffic logs from urban roads. For real-world projects, you can use:
  - [Kaggle Traffic Datasets](https://www.kaggle.com/datasets)  
  - Open government traffic/transportation APIs  
  - GPS logs from city or vehicle telemetry (ensure privacy compliance)

---

    How It Works

1.   Upload Data  : Upload a CSV file or use the included sample.  
2.   Preprocessing  : The app parses timestamps, handles missing values, and computes additional features (hour, weekday, etc.).  
3.   Hotspot Detection  : DBSCAN clusters high-density points; clusters are assigned severity scores based on:
   - Number of points  
   - Number of incidents  
   - Average speed (lower speed → higher congestion)  
4.   Visualization  : Hotspots are displayed on an interactive map with circle markers sized by severity. Heatmaps show overall density.  
5.   Time Analysis  : Charts display hourly and weekday trends to understand peak traffic times.  
6.   Export  : Hotspot summaries can be downloaded as CSV for further use.  

---

    Quick Start

    Local Setup

1. Clone repository:
```bash
git clone <your-repo-url>
cd traffic-hotspot-analyzer
