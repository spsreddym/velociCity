import folium
from folium.plugins import MarkerCluster, HeatMap
import plotly.express as px
from streamlit_folium import folium_static

def create_map(df, clusters_df=None, start_coords=(20.5937,78.9629), zoom_start=6):
    m = folium.Map(location=start_coords, zoom_start=zoom_start, control_scale=True)
    marker_cluster = MarkerCluster(name="Data points", options={'maxClusterRadius':30}).add_to(m)
    for _,row in df.iterrows():
        folium.CircleMarker(
            location=(row["latitude"], row["longitude"]),
            radius=2,
            fill=True,
            fill_opacity=0.6,
            popup=f"{row.get('timestamp','')}: speed={row.get('speed','')}"
        ).add_to(marker_cluster)
    heat_data = df[["latitude","longitude"]].values.tolist()
    HeatMap(heat_data, radius=15).add_to(m)
    if clusters_df is not None and not clusters_df.empty:
        for _,c in clusters_df.iterrows():
            severity = float(c["severity"])
            folium.Circle(
                location=(c["lat_mean"],c["lon_mean"]),
                radius=100+severity*400,
                color="crimson",
                fill=True,
                fill_opacity=0.4,
                popup=f"Cluster {int(c['cluster'])} — severity: {severity:.2f}, count: {int(c['count'])}"
            ).add_to(m)
    folium.LayerControl().add_to(m)
    return m

def show_map_in_streamlit(m):
    folium_static(m, width=700, height=500)

def plot_hourly_pattern(hourly_df):
    fig = px.bar(hourly_df, x="hour", y="count", title="Records by Hour of Day")
    return fig

def plot_weekday_pattern(weekday_df):
    wd_map={0:"Mon",1:"Tue",2:"Wed",3:"Thu",4:"Fri",5:"Sat",6:"Sun"}
    df = weekday_df.copy()
    df["weekday_name"] = df["weekday"].map(wd_map)
    fig = px.bar(df, x="weekday_name", y="count", title="Records by Weekday")
    return fig
