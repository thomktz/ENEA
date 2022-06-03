# %%
from matplotlib.lines import Line2D
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression


model_df = pd.read_csv("MODEL_DF.csv")


X = model_df[["before_crash_frequency", 
              "initial_speed", 
              "speed_delta", 
              "before_severity", 
              "average_wetness", 
              "average_vehicule_volume"]]

X_mean, X_std = X.mean(), X.std()
X = (X-X_mean)/X_std

y = model_df["after_crash_frequency"]
y_mean, y_std = y.mean(), y.std()
y = (y-y_mean)/y_std




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



##############
# %% Logistic Regression

def fit_LinearRegression(X, y):
    estimator = LinearRegression()
    estimator.fit(X, y)
    print(estimator.coef_)
    return estimator

def fit_sm_LinearRegression(X, y):
    X = sm.add_constant(X)
    estimator = sm.OLS(y, X)
    result = estimator.fit()
    print(result.summary())
    return estimator
# %%
