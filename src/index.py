from modules.manipulation import  check_and_convert_to_csv
from modules.preprocessing import replace_error_value, remove_outliers_iqr, min_max_scale
from modules.training import model_linear_regression
from modules.evaluation import evaluate
from modules.save import save_model, load_model

from config import input_columns, output_columns

import pandas as pd
from sklearn.model_selection import train_test_split    

# convert xlsx to csv
# check_and_convert_to_csv(r"D:\Test\AI_measure\src\data\raw\dataset_measure.xlsx", r"D:\Test\AI_measure\src\data\processed\dataset_measure.csv")

df = pd.read_csv(r"D:\Test\AI_measure\src\data\processed\dataset_measure.csv")

# convert to number
df = df.apply(pd.to_numeric, errors='coerce') 
df = df.apply(lambda col: replace_error_value(col, ["gender", "form"]))
df.fillna(df.mean(),  inplace=True)
df = df.round(1)

# eliminate outlier data
for column in df.columns:
    df = remove_outliers_iqr(df, column) 

# normalize dataframe
df = min_max_scale(df)

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

# save model

save_model(model, r"D:\Test\AI_measure\src\models\linear_model.pkl")
