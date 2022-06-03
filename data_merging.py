# %% Imports
import pandas as pd
import numpy as np

# Variables
FOLDER = "ACCIDENT/"
KEY = "ACCIDENT_NO"

### Opening and treatment of the default database
df_ACCIDENT = pd.read_csv(FOLDER + "ACCIDENT.csv").set_index(KEY)
df_ACCIDENT = df_ACCIDENT.drop(columns=["ACCIDENT_TYPE",
                          "DAY_OF_WEEK", 
                          "DCA_CODE",
                          "POLICE_ATTEND",
                          "ROAD_GEOMETRY", 
                          "PAGE", 
                          "LIGHT_CONDITION",
                          "DIRECTORY",
                          "EDITION",
                          "GRID_REFERENCE_X", 
                          "GRID_REFERENCE_Y"])
df_ACCIDENT.ACCIDENTDATE = pd.to_datetime(df_ACCIDENT.ACCIDENTDATE)
df_ACCIDENT["YEAR"] = df_ACCIDENT.ACCIDENTDATE.dt.year


df_NODE = pd.read_csv(FOLDER + "NODE.csv").set_index(KEY)
df_NODE = df_NODE[["Lat", "Long"]]


df_ATMOSHPERIC = pd.read_csv(FOLDER + "ATMOSPHERIC_COND.csv").set_index(KEY)
df_ATMOSHPERIC = df_ATMOSHPERIC[["Atmosph Cond Desc"]]

df_LOCATION = pd.read_csv(FOLDER + "ACCIDENT_LOCATION.csv").set_index(KEY)
df_LOCATION = df_LOCATION[["ROAD_ROUTE_1", "ROAD_NAME", 
                           "ROAD_TYPE", "ROAD_NAME_INT", 
                           "ROAD_TYPE_INT"]]

df_ROAD_SURFACE = pd.read_csv(FOLDER +"ROAD_SURFACE_COND.csv").set_index(KEY)
df_ROAD_SURFACE["SURFACE_COND"] = df_ROAD_SURFACE["SURFACE_COND"] - 1
df_ROAD_SURFACE = df_ROAD_SURFACE[["SURFACE_COND"]]

# Merging files
df = pd.merge(df_ACCIDENT, df_NODE, how="inner", left_index=True, right_index=True)
df = pd.merge(df, df_ATMOSHPERIC, how="inner", left_index=True, right_index=True)
df = pd.merge(df, df_LOCATION, how="inner", left_index=True, right_index=True)
df = pd.merge(df, df_ROAD_SURFACE, how="inner", left_index=True, right_index=True)

### Additional ata
df_TRAFFIC = pd.read_csv("Traffic_Volume.csv")
df_TRAFFIC = df_TRAFFIC[["ROAD_NBR", "LOCAL_ROAD_NM", 
                         "ALLVEHS_AADT"]]

df_TRAFFIC["ROAD_NAME"] = df_TRAFFIC["LOCAL_ROAD_NM"].apply(lambda x:" ".join(x.split(" ")[0:-1]))
df_TRAFFIC["ROAD_TYPE"] = df_TRAFFIC["LOCAL_ROAD_NM"].apply(lambda x:"".join(x.split(" ")[-1]))
df_TRAFFIC["ROAD_ROUTE_1"] = df_TRAFFIC["ROAD_NBR"]
df_TRAFFIC = df_TRAFFIC.drop(columns="ROAD_NBR")
df_TRAFFIC = df_TRAFFIC.groupby(["ROAD_NAME", "ROAD_TYPE", "ROAD_ROUTE_1"]).mean().reset_index()

df_ACCIDENTS_PER_ROADS = df.reset_index().groupby(["ROAD_NAME", "ROAD_TYPE", "ROAD_ROUTE_1"])[KEY].count().reset_index()
df_ACCIDENTS_PER_ROADS = pd.merge(df_ACCIDENTS_PER_ROADS, df_TRAFFIC, on = ("ROAD_NAME", "ROAD_TYPE", "ROAD_ROUTE_1"))
df_ACCIDENTS_PER_ROADS["ACCIDENT_RATE"] = df_ACCIDENTS_PER_ROADS["ACCIDENT_NO"]/df_ACCIDENTS_PER_ROADS["ALLVEHS_AADT"]
df_ACCIDENTS_PER_ROADS["ACCIDENT_RATE"] = df_ACCIDENTS_PER_ROADS["ACCIDENT_RATE"].clip(upper=0.1)
df_ACCIDENTS_PER_ROADS = df_ACCIDENTS_PER_ROADS.drop(columns=["ACCIDENT_NO"])

#%%
df = pd.merge(df, df_ACCIDENTS_PER_ROADS, on = ("ROAD_NAME", "ROAD_TYPE", "ROAD_ROUTE_1"))
df = df.sort_values("ACCIDENTDATE")


