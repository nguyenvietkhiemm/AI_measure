from modules.manipulation import  check_and_convert_to_csv
from modules.preprocessing import replace_error_value, remove_outliers_iqr, min_max_scale
from modules.training import model_linear_regression
from modules.evaluation import evaluate
from modules.save import save_model, load_model
from modules.extract_js import extract_js

from config import input_columns, output_columns, json_model_path

import pandas as pd
from sklearn.model_selection import train_test_split    

from pathlib import Path

# convert xlsx to csv
check_and_convert_to_csv(Path(r"data\raw\dataset_measure.xlsx").resolve(), Path(r"data\raw\dataset_measure.csv").resolve())

df = pd.read_csv(Path(r"data\raw\dataset_measure.csv").resolve())

# convert to number
df = df.apply(pd.to_numeric, errors='coerce') 
df = df.apply(lambda col: replace_error_value(col, ["gender", "form"]))
df.fillna(df.mean(),  inplace=True)
df = df.round(1)

# eliminate outlier data
for column in df.columns:
    df = remove_outliers_iqr(df, column) 

# save data
df.to_csv(Path(r"data\processed\dataset_measure.csv").resolve(), index=False)

# normalize dataframe
df, min_max_scaler = min_max_scale(df)

#split data
X = df[input_columns]
y = df[output_columns]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# train
model = model_linear_regression(X_train, y_train)

# predict
y_pred = model.predict(X_test)

# evaluate
mae, mse, rmse, r2 = evaluate(y_test, y_pred)

print("MAE: ", mae)
print("MSE: ", mse)
print("RMSE: ", rmse)
print("R2: ", r2)

# save dataframe
test = pd.DataFrame(min_max_scaler.inverse_transform(pd.concat([pd.DataFrame(X_test), pd.DataFrame(y_test)], axis=1)))
pred = pd.DataFrame(min_max_scaler.inverse_transform(
    pd.concat([pd.DataFrame(X_test).reset_index(drop=True), pd.DataFrame(y_pred).reset_index(drop=True)], axis=1)
))
metrics = pd.DataFrame({"MAE": [mae], "MSE": [mse], "RMSE": [rmse], "R2": [r2]})

test.to_csv(Path(r"results\dataframe\test.csv").resolve(), index=False)
pred.to_csv(Path(r"results\dataframe\pred.csv").resolve(), index=False)
metrics.to_csv(Path(r"results\metrics\metric.csv").resolve(), index=False)

# save model
save_model(model, Path(r"models\linear_model.pkl").resolve())

#extract json
extract_js(json_model_path, model, min_max_scaler)