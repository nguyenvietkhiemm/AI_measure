import os
import numpy as np
from modules.manipulation import check_and_convert_to_csv, check_csv
from modules.preprocessing import replace_error_value, remove_outliers_iqr, min_max_scale
from modules.Models import LinearRegressionModel, LightGBMModel
from modules.evaluation import evaluate
from modules.save import save_model, load_model
from modules.extract_js import extract_js
from modules.run_notebooks import run_notebooks

from config import input_columns, output_columns, json_model_path

import pandas as pd
from sklearn.model_selection import train_test_split    

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    # PATH
    dataset_xlsx = os.path.join(ROOT_DIR, "data", "raw", "dataset_measure.xlsx")
    dataset_csv = os.path.join(ROOT_DIR, "data", "raw", "dataset_measure.csv")
    processed_csv = os.path.join(ROOT_DIR, "data", "processed", "dataset_measure.csv")
    test_csv = os.path.join(ROOT_DIR, "results", "dataframe", "test.csv")
    pred_csv = os.path.join(ROOT_DIR, "results", "dataframe", "pred.csv")
    metrics_csv = os.path.join(ROOT_DIR, "results", "metrics", "metric.csv")
    model_path = os.path.join(ROOT_DIR, "models", "linear_model.pkl")
    index_js = os.path.join(ROOT_DIR, "js", "index.js")
    notebooks_path = os.path.join(ROOT_DIR, "notebooks", "analysis.ipynb")

    # convert xlsx to csv
    # check_and_convert_to_csv(dataset_xlsx, dataset_csv)
    
    # check_csv
    check_csv(dataset_csv)

    df = pd.read_csv(dataset_csv)

    # convert to number
    df = df.apply(pd.to_numeric, errors='coerce') 
    # df = df.apply(lambda col: replace_error_value(col, ["gender", "form"]))
    df = df.apply(lambda col: replace_error_value(col, ["Gender"]))
    df.fillna(df.mean(), inplace=True)
    df = df.round(1)

    # eliminate outlier data
    for column in df.columns:
        df = remove_outliers_iqr(df, column) 

    # save data
    df.to_csv(processed_csv, index=False)

    # normalize dataframe
    normalized_df, min_max_scaler = min_max_scale(df)

    #split data
    X = normalized_df[input_columns]
    y = normalized_df[output_columns]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    # train
    # model = LightGBMModel()
    model = LinearRegressionModel()
    
    model.train(X_train, y_train)
    # model = model_lightgbm(X_train, y_train)

    # predict
    y_pred = model.predict(X_test)
    
    # recover
    test = pd.concat([pd.DataFrame(X_test), pd.DataFrame(y_test)], axis=1)
    pred = pd.concat([pd.DataFrame(X_test).reset_index(drop=True), pd.DataFrame(y_pred).reset_index(drop=True)], axis=1)
    
    # recover X_test and y_test (inverse transform)
    test = pd.DataFrame(min_max_scaler.inverse_transform(np.concatenate([X_test, y_test], axis=1)),
                                columns=input_columns + output_columns)

    pred = pd.DataFrame(min_max_scaler.inverse_transform(np.concatenate([X_test, y_pred], axis=1)),
                                columns=input_columns + output_columns)

    # evaluate
    mae, mse, rmse, r2 = evaluate(test[output_columns], pred[output_columns])
    
    cases_number = len(test)

    print("\nSai số trung bình cho {} trường hợp: ".format(cases_number), mae, "\n")
    print("MAE: ", mae)
    print("MSE: ", mse)
    print("RMSE: ", rmse)
    print("R2: ", r2)

    # save dataframe

    metrics = pd.DataFrame({"MAE": [mae], "MSE": [mse], "RMSE": [rmse], "R2": [r2]})

    test.to_csv(test_csv, index=False)
    pred.to_csv(pred_csv, index=False)
    metrics.to_csv(metrics_csv, index=False)

    # save model
    save_model(model.get_model(), model_path)

    #extract json
    extract_js(json_model_path, index_js, model.get_model(), min_max_scaler)
    
    #run notebooks
    run_notebooks(notebooks_path)

if __name__ == "__main__":
    main()
