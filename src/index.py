import os
import numpy as np
from modules.manipulation import check_and_convert_to_csv, check_csv
from modules.preprocessing import replace_error_value, remove_outliers_iqr, min_max_scale
from modules.Models import LinearRegressionModel, LightGBMModel
from modules.evaluation import evaluate
from modules.save import save_model, load_model
from modules.run_notebooks import run_notebooks

from config import input_columns, output_columns, js_model_path

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
    check_and_convert_to_csv(dataset_xlsx, dataset_csv)
    
    # check_csv
    check_csv(dataset_csv)

    df = pd.read_csv(dataset_csv)
    
    df = df[input_columns + output_columns]

    # convert to number
    df = df.apply(pd.to_numeric, errors='coerce') 
    df = df.apply(lambda col: replace_error_value(col, ["gender", "form"]))
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
    model.train_all_combinations(X_train, y_train, input_columns, output_columns)
    
    # test dataframe
    test = pd.concat([pd.DataFrame(X_test), pd.DataFrame(y_test)], axis=1)
    test_inverse = pd.DataFrame(min_max_scaler.inverse_transform(test), 
                            columns=input_columns + output_columns)

    # evaluate
    metrics = pd.DataFrame({"Input": [], "Output":[], "MAE": [], "MSE": [], "RMSE": [], "R2": []})
    current_input_columns = input_columns.copy()
    for output_column in output_columns[:-1]:
        current_input_columns.append(output_column)
        # predict
        print("================================================================================================")
        y_pred = model.predict(test[current_input_columns])
        current_output_columns = [col for col in output_columns if col not in current_input_columns]
        
        pred = pd.concat([pd.DataFrame(test[current_input_columns]).reset_index(drop=True), pd.DataFrame(y_pred).reset_index(drop=True)], axis=1)
        pred_inverse = pd.DataFrame(min_max_scaler.inverse_transform(pred),
                            columns=current_input_columns + current_output_columns)

        mae, mse, rmse, r2 = evaluate(test_inverse[current_output_columns], pred_inverse[current_output_columns])

        print("Average error for {} cases of inputs: {} ==> outputs: {}".format(len(test), current_input_columns, current_output_columns))
        print("MAE: ", mae)
        print("MSE: ", mse)
        print("RMSE: ", rmse)
        print("R2: ", r2)
        print("================================================================================================\n\n")
        
            # Thêm dữ liệu vào DataFrame metrics
        metrics = metrics._append({
            "Input": ", ".join(current_input_columns),
            "Output": ", ".join(current_output_columns),
            "MAE": mae,
            "MSE": mse,
            "RMSE": rmse,
            "R2": r2
        }, ignore_index=True)
        
    # save dataframe
    test_inverse.to_csv(test_csv, index=False)
    pred.to_csv(pred_csv, index=False)
    metrics.to_csv(metrics_csv, index=False)

    # save model
    save_model(model.get_models(), model_path)

    #extract json
    model.extract_js(js_model_path, index_js, min_max_scaler)
    
    #run notebooks
    run_notebooks(notebooks_path)

if __name__ == "__main__":
    main()
