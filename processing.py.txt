import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN

def load_data(path_or_df):
    if isinstance(path_or_df, pd.DataFrame):
        return path_or_df.copy()
    return pd.read_csv(path_or_df)

def preprocess(df, timestamp_col="timestamp"):
    df = df.copy()
    df = df.dropna(subset=["latitude","longitude"])
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce')
    df = df.dropna(subset=[timestamp_col])
    df["year"] = df[timestamp_col].dt.year
    df["month"] = df[timestamp_col].dt.month
    df["day"] = df[timestamp_col].dt.day
    df["hour"] = df[timestamp_col].dt.hour
    df["weekday"] = df[timestamp_col].dt.weekday
    df["speed"] = pd.to_numeric(df.get("speed",-1), errors="coerce").fillna(-1)
    df["incident"] = pd.to_numeric(df.get("incident",0), errors="coerce").fillna(0).astype(int)
    return df

def detect_hotspots_dbscan(df, eps_meters=50, min_samples=5):
    df = df.copy()
    coords = np.radians(df[["latitude","longitude"]].values)
    eps = eps_meters/6371000
    db = DBSCAN(eps=eps, min_samples=min_samples, metric="haversine")
    labels = db.fit_predict(coords)
    df["cluster"] = labels
    clusters = df[df["cluster"]!=-1].groupby("cluster").agg(
        count=("cluster","size"),
        avg_speed=("speed", lambda x: x[x>=0].mean() if (x>=0).any() else np.nan),
        incidents=("incident","sum"),
        lat_mean=("latitude","mean"),
        lon_mean=("longitude","mean")
    ).reset_index()
    if not clusters.empty:
        c_min,c_max = clusters["count"].min(), clusters["count"].max()
        clusters["count_norm"] = (clusters["count"]-c_min)/(c_max-c_min+1e-6)
        inc_min,inc_max = clusters["incidents"].min(), clusters["incidents"].max()
        clusters["inc_norm"] = (clusters["incidents"]-inc_min)/(inc_max-inc_min+1e-6)
        sp = clusters["avg_speed"].fillna(clusters["avg_speed"].mean() if clusters["avg_speed"].notna().any() else 0)
        sp_min, sp_max = sp.min(), sp.max()
        clusters["speed_norm"] = 1 - ((sp-sp_min)/(sp_max-sp_min+1e-6))
        clusters["severity"] = 0.5*clusters["count_norm"] + 0.3*clusters["inc_norm"] + 0.2*clusters["speed_norm"]
        clusters = clusters.sort_values("severity",ascending=False).reset_index(drop=True)
    else:
        clusters["severity"] = []
    return df, clusters

def aggregate_time_patterns(df):
    df = df.copy()
    hourly = df.groupby("hour").size().rename("count").reset_index()
    weekday = df.groupby("weekday").size().rename("count").reset_index()
    return hourly, weekday

def export_hotspot_summary(clusters_df, path="hotspots_summary.csv"):
    clusters_df.to_csv(path,index=False)
    return path
