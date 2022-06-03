from model_augmented_dataset import fit_RandomForest, X, y
from utils import access_road
from data_merging import df

estimator = fit_RandomForest(X,y)

def predict(road_name, road_type, road_nb):
    """
    Since we never look at the metrics, the whole dataset is used as training. 
    """
    sub_df = access_road(df, road_name, road_type, road_nb)
    sub_df = sub_df[sub_df["SPEED_ZONE"] < 200]

    X_pred = sub_df[["SPEED_ZONE","ALLVEHS_AADT","SURFACE_COND"]].mean()
    #y = sub_df["ACCIDENT_RATE"].mean()
    
    
    return estimator.predict(X_pred)

def predict_with_delta(delta, road_name, road_type, road_nb):
    sub_df = access_road(df, road_name, road_type, road_nb)
    sub_df = sub_df[sub_df["SPEED_ZONE"] < 200]
    sub_df["SPEED_ZONE"] = sub_df["SPEED_ZONE"] + delta
    X_pred = sub_df[["SPEED_ZONE","ALLVEHS_AADT","SURFACE_COND"]].mean()
    
    return estimator.predict(X_pred)