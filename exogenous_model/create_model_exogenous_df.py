# %%
from utils import access_road, keys, start_date, end_date
from data_merging import df
import numpy as np
import pandas as pd


def create_model_df(df):
    
    
    categories = dict(road = [],
                    before_crash_frequency = [],
                    after_crash_frequency = [],
                    initial_speed = [],
                    speed_delta = [],
                    before_severity = [],
                    after_severity = [],
                    average_wetness = [],
                    average_vehicule_volume = [],
                    )

    for i, key in enumerate(keys):

        sub_df = access_road(df, *key)
        sub_df = sub_df[sub_df["SPEED_ZONE"] < 200]
        if (sub_df["SPEED_ZONE"].is_monotonic_increasing or sub_df["SPEED_ZONE"].is_monotonic_decreasing) and  sub_df["SPEED_ZONE"].nunique() > 1:
            
            
            ### We want to find the speed change that best splits the data for each road
            sub_df["Change"] = (sub_df['SPEED_ZONE'].diff() != 0)
            sub_df["Change"].iloc[0] = False
        
            i = 0
            n = sub_df.shape[0]
            difference_to_middle = []
            i_list = []
            for index, row in sub_df.iterrows():
                if row.Change:
                    difference_to_middle.append(abs(i - n/2))
                    i_list.append(i)
                i += 1
            difference_to_middle = np.array(difference_to_middle)
            best_split = i_list[np.argmin(difference_to_middle)]
            
            
            before_df = sub_df.iloc[:best_split]
            after_df = sub_df.iloc[best_split:]
            
            ### We'll assume that the change in speeds happenend 
            ### right in the middle of the split
            last_before_date = before_df.iloc[-1]["ACCIDENTDATE"]
            first_after_date = after_df.iloc[0]["ACCIDENTDATE"]
            
            mid_point = pd.Interval(last_before_date, first_after_date).mid
        

            before_period_length = pd.Interval(start_date, last_before_date).length.days
            after_period_length = pd.Interval(first_after_date, end_date).length.days
            
            before_crash_frequency = before_df.shape[0]/before_period_length
            after_crash_frequency = after_df.shape[0]/after_period_length
            
            speed_delta = after_df["SPEED_ZONE"].mean() - before_df["SPEED_ZONE"].mean()
            
            before_severity = before_df["SEVERITY"].mean()
            after_severity = after_df["SEVERITY"].mean()
            
            average_wetness = sub_df[sub_df["SURFACE_COND"]<2]["SURFACE_COND"].mean()
            
            average_vehicule_volume = sub_df["ALLVEHS_AADT"].mean()
            
            categories["road"].append(" ".join([str(e) for e in key]))
            categories["before_crash_frequency"].append(before_crash_frequency)
            categories["after_crash_frequency"].append(after_crash_frequency)
            categories["initial_speed"].append(before_df["SPEED_ZONE"].mean())
            categories["speed_delta"].append(speed_delta)
            categories["before_severity"].append(before_severity)
            categories["after_severity"].append(after_severity)
            categories["average_wetness"].append(average_wetness)
            categories["average_vehicule_volume"].append(average_vehicule_volume)
            

    model_df = pd.DataFrame(categories)
    return model_df

if __name__ == '__main__':
    model_df = create_model_df(df)
    model_df.to_csv("MODEL_DF.csv", index=False)
    
    
        

# %%
