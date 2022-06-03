# %%
from data_merging import df

start_date= df["ACCIDENTDATE"].min()
end_date = df["ACCIDENTDATE"].max()

def access_road(df, road_name, road_type, road_number):
    return df[(df["ROAD_NAME"] == road_name) & (df["ROAD_TYPE"] == road_type) & (df["ROAD_ROUTE_1"] == road_number)]

keys = list(df.groupby(["ROAD_NAME", "ROAD_TYPE", "ROAD_ROUTE_1"]).groups.keys())