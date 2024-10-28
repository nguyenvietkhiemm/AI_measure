import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsRegressor

def replace_error_value_by_nan(column, except_columns):
    if column.name not in except_columns:
        column = column.mask((column < 10) | (column > 250), np.nan)
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

def label_encode(df, column):
    label_encoder = LabelEncoder()
    df[column] = label_encoder.fit_transform(df[column])
    return df, label_encoder

def fill_missing_data_by_knn(df, input_columns, columns, n_neighbors=10):
    for column in columns:
        _columns = input_columns + [column]
        df_missing = df[df[column].isna()][_columns]
        df_valid = df[df[column].notna()][_columns]
        if df_valid.empty or df_missing.empty:
            continue
        knn = KNeighborsRegressor(n_neighbors)
        knn.fit(df_valid[input_columns], df_valid[column])
        predicted_values = knn.predict(df_missing[input_columns])
        df.loc[pd.isna(df[column]), column] = predicted_values
    return df