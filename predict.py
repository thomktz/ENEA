# %%
from model import fit_LinearRegression, X, y, fit_RandomForest
from data_merging import df
from utils import access_road, keys, start_date, end_date
import pandas as pd
import numpy as np
import statsmodels.api as sm
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "notebook_connected"

estimator = fit_RandomForest(X, y)
period_length = pd.Interval(start_date, end_date).length.days

# %%
def predict(speed_delta, road_name, road_type, road_nb):
    sub_df = access_road(df, road_name, road_type, road_nb)
    sub_df = sub_df[sub_df["SPEED_ZONE"] < 200]

    speed = sub_df["SPEED_ZONE"].mean()
    crash_frequency = sub_df.shape[0]/period_length
    before_severity = sub_df["SEVERITY"].mean()
    average_wetness = sub_df[sub_df["SURFACE_COND"]<2]["SURFACE_COND"].mean()
    average_vehicule_volume = sub_df["ALLVEHS_AADT"].mean()
    
    
    X_oos = pd.DataFrame(dict(
                            before_crash_frequency=[crash_frequency], 
                            initial_speed = speed,
                            speed_delta = -speed_delta, 
                            before_severity = before_severity,  
                            average_wetness = average_wetness, 
                            average_vehicule_volume = average_vehicule_volume))
    


    
    return estimator.predict(X_oos)
    
key = ("ALBION", "STREET", 5867)
    
Delta_speeds = np.linspace(-60, 60, num=12)
preds = [predict(delta, *key)[0] for delta in Delta_speeds]
df_results = pd.DataFrame({"accident_rate_evol":preds, "speed_delta":Delta_speeds})

px.line(df_results, x = "speed_delta", y = "accident_rate_evol")
 # %%
