from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

def model_linear_regression(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    return model