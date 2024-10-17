import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def replace_error_value(column, except_columns):
    if column.name not in except_columns:
        column = column.mask((column < 10) | (column > 250), np.nan)
        column = column.fillna(column.mean())
    return column

# Xác định outliers bằng IQR
def remove_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.01)
    Q3 = df[column].quantile(0.99)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

def min_max_scale(df):
    min_max_scaler = MinMaxScaler(feature_range=(0, 1))
    df_min_max_scaled = pd.DataFrame(min_max_scaler.fit_transform(df), columns=df.columns)
    return df_min_max_scaled, min_max_scaler
