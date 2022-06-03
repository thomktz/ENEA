# %%
from data_merging import df
import pandas as pd
import plotly.express as px
import plotly.io as pio
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

from model_exogenous import fit_LinearRegression
pio.renderers.default = "notebook_connected"

usable_df = df[(df["SPEED_ZONE"]<200) & (df["SURFACE_COND"]<2)]

df_grouped = usable_df.groupby(["ROAD_NAME", "ROAD_TYPE", "ROAD_ROUTE_1"]).agg({"SPEED_ZONE":"mean",
                                                                            "ACCIDENT_RATE":"mean",
                                                                            "ALLVEHS_AADT":"mean",
                                                                            "SURFACE_COND":"mean"})

#px.scatter(df_grouped, x = "MEAN_SPEED_OF_ROAD", y = "ACCIDENT_RATE", trendline="ols", title="<b>OLS Regression:</b> Accident rate on the average speed per road<br>Y = -0.23 + 0.0058 * X")


# %%
param_grid = { 
    'n_estimators': [200, 500],
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth' : [4,5,6,7,8]
}

def fit_RandomForest(X, y):
    estimator = RandomForestRegressor()
    grid = GridSearchCV(estimator, param_grid)
    grid.fit(X, y)
    return grid

X = df_grouped[["SPEED_ZONE", "ALLVEHS_AADT", "SURFACE_COND"]]
y = df_grouped["ACCIDENT_RATE"]

grid = fit_RandomForest(X, y)
# %%
