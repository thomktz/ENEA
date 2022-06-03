# %%
from data_merging import df
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "notebook_connected"

GRAPHS_FOLDER = "graphs/"
#%%
fig = px.density_mapbox(df, lat='Lat', lon='Long', z='SEVERITY', radius=2,
                        center=dict(lat=-36, lon=144), zoom=5,
                        mapbox_style="stamen-terrain",
                        animation_frame="YEAR",
                        hover_data=["SPEED_ZONE", "ROAD_ROUTE_1", "ROAD_NAME",
                                    "ROAD_TYPE", "ROAD_NAME_INT", 
                                    "ROAD_TYPE_INT", "ACCIDENT_RATE"])
fig.show()
with open(GRAPHS_FOLDER+'out_density_animation.html', "w") as f:
    f.write(fig.to_html())
    
fig = px.density_mapbox(df, lat='Lat', lon='Long', z='SEVERITY', radius=2,
                        center=dict(lat=-36, lon=144), zoom=5,
                        mapbox_style="stamen-terrain",
                        hover_data=["YEAR", "SPEED_ZONE", "ROAD_ROUTE_1", "ROAD_NAME",
                                    "ROAD_TYPE", "ROAD_NAME_INT", 
                                    "ROAD_TYPE_INT", "ACCIDENT_RATE"])
fig.show()
with open(GRAPHS_FOLDER+'out_density.html', "w") as f:
    f.write(fig.to_html())

fig = px.scatter_mapbox(df, lat='Lat', lon='Long', color='ACCIDENT_RATE',
                        center=dict(lat=-36, lon=144), zoom=5,
                        mapbox_style="stamen-terrain",
                        hover_data=["SEVERITY", "ROAD_ROUTE_1", "ROAD_NAME",
                                    "ROAD_TYPE", "ROAD_NAME_INT", 
                                    "ROAD_TYPE_INT", "ACCIDENT_RATE"])
fig.show()
with open(GRAPHS_FOLDER+'out_scatter.html', "w") as f:
    f.write(fig.to_html())
#%%
df.loc[df["ALLVEHS_AADT"]>30000, "ALLVEHS_AADT"] = 30000
fig = px.scatter_mapbox(df, lat='Lat', lon='Long', color='ALLVEHS_AADT',
                        center=dict(lat=-36, lon=144), zoom=5,
                        mapbox_style="stamen-terrain",
                        title="Traffic volume (2020)",
                        hover_data=["SEVERITY", "ROAD_ROUTE_1", "ROAD_NAME",
                                    "ROAD_TYPE", "ROAD_NAME_INT", 
                                    "ROAD_TYPE_INT", "ACCIDENT_RATE"])
fig.show()
with open(GRAPHS_FOLDER+'volume.html', "w") as f:
    f.write(fig.to_html())


# %%
df = df[df["SPEED_ZONE"]<200]
df_raw = df.groupby(["ROAD_NAME", "ROAD_TYPE", "ROAD_ROUTE_1"]).agg({"SPEED_ZONE":"mean","NODE_ID":"size"})
df_raw["NB_ACCIDENTS_OF_ROAD"] = df_raw["NODE_ID"]
df_raw["MEAN_SPEED_OF_ROAD"] = df_raw["SPEED_ZONE"]

px.scatter(df_raw, x = "MEAN_SPEED_OF_ROAD", y = "NB_ACCIDENTS_OF_ROAD", trendline="ols", title="<b>OLS Regression:</b> Number of accidents on the average speed per road<br>Y = 70.2 - 0.08 * X")
# %%
df = df[df["SPEED_ZONE"]<200]

df_raw = df.groupby(["ROAD_NAME", "ROAD_TYPE", "ROAD_ROUTE_1"]).agg({"SPEED_ZONE":"mean","ACCIDENT_RATE":"mean"})
df_raw["ACCIDENT_RATE"] = df_raw["ACCIDENT_RATE"] * 10
df_raw["MEAN_SPEED_OF_ROAD"] = df_raw["SPEED_ZONE"]

px.scatter(df_raw, x = "MEAN_SPEED_OF_ROAD", y = "ACCIDENT_RATE", trendline="ols", title="<b>OLS Regression:</b> Accident rate on the average speed per road<br>Y = -0.23 + 0.0058 * X")
# %%
