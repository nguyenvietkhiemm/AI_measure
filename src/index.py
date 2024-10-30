import os
import sys
import numpy as np
from dotenv import load_dotenv
from modules.manipulation import check_and_convert_to_csv, check_csv
from modules.preprocessing import replace_error_value_by_nan, remove_outliers_iqr, min_max_scale, label_encode, fill_missing_data_by_knn
from modules.Models import LinearRegressionModel, LightGBMModel
from modules.evaluation import evaluate
from modules.get_data import get_api_data_post
from modules.save import save_model, load_model
from modules.run_notebooks import run_notebooks
from modules.examples import create_data

from config import input_columns, output_columns, discrete_columns, split_column, js_model_path

import pandas as pd
from sklearn.model_selection import train_test_split

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_ROOT_DIR = os.path.dirname(ROOT_DIR)

load_dotenv()

numeric_columns = list(set(input_columns + output_columns) - set(discrete_columns))
discrete_columns = [col for col in discrete_columns if col not in split_column]

# def sqr_df(df, numeric_columns):
#     for column in list(numeric_columns):
#         df[column] = df[column] ** 2
#     return df

# def sqrt_df(df, numeric_columns):
#     for column in list(numeric_columns):
#         df[column] = np.sqrt(df[column])
#     return df

def preprocessing(dataset_csv, save_csv=None):
    try:
        save_csv = save_csv or dataset_csv
        columns_encoder = {}
        check_csv(dataset_csv)
        df = pd.read_csv(dataset_csv)
        df = df[input_columns + output_columns]
        for column in list(df.columns):
            if column not in discrete_columns:
                df[column] = df[column].str.replace(",", ".").apply(pd.to_numeric, errors='coerce')
        df = df.apply(lambda col: replace_error_value_by_nan(col, except_columns=discrete_columns))
        df = df.dropna(thresh=int(df.shape[1] * 0.5))
        df = fill_missing_data_by_knn(df, input_columns=input_columns, columns=output_columns)
        print("HAHA", discrete_columns)
        for column in discrete_columns:
            df, label_encoder = label_encode(df, column)
            columns_encoder.update({column: list(label_encoder.classes_)})
        for column in df.columns:
            df = remove_outliers_iqr(df, column)   
        df.to_csv(save_csv, index=False)
        
        return df, columns_encoder
    except Exception as e:
        print(f"Error occurred while processing: {dataset_csv} {e}")
        

        
def split_data(df, split_column, save_dir):
    if split_column not in df.columns:
        print(f"Df has no split column: {split_column}")
        df[split_column] = "None"
    
    df[split_column] = df[split_column].fillna("None")
    split_dfs = {value: df[df[split_column] == value] for value in df[split_column].unique()}
    for value, df in split_dfs.items():
        df.drop(split_column, axis=1).to_csv(os.path.join(save_dir, "{}_{}.csv").format(split_column, value), index=False)
        
def clear_files(dir):
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        try:
            if os.path.isfile(file_path):  # Kiểm tra nếu là tệp
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

def main():
    # PATH
    # default
    raw_dataset_dir = os.path.join(PARENT_ROOT_DIR, "data", "raw")
    processed_dir = os.path.join(PARENT_ROOT_DIR, "data", "processed")
    merged_dataset_csv = os.path.join(PARENT_ROOT_DIR, "data", "raw", "__merged_raw_data.csv")

    # api data file path
    dataset_api_csv = os.path.join(PARENT_ROOT_DIR, "data", "raw", "dataset_measure_api.csv")

    test_csv = os.path.join(ROOT_DIR, "results", "dataframe", "test.csv")
    pred_path = os.path.join(ROOT_DIR, "results", "dataframe", "pred")
    metrics_csv = os.path.join(ROOT_DIR, "results", "metrics", "metric.csv")
    model_path = os.path.join(ROOT_DIR, "models", "linear_model.pkl")
    index_js = os.path.join(ROOT_DIR, "js", "index.js")
    notebooks_path = os.path.join(ROOT_DIR, "notebooks", "analysis.ipynb")

    try:
        # get api data
        print("Fetching data from API...")
        get_api_data_post(url=os.getenv('API_URL'), data={
            "access_key": os.getenv('ACCESS_KEY'),
            "access_token": os.getenv('ACCESS_TOKEN'),
        }, dataset_csv=dataset_api_csv, input_columns = input_columns, output_columns = output_columns)
    except Exception as e:
        print(f"Error fetching API data: {e}")

    raw_dataset_files = [f for f in os.listdir(raw_dataset_dir) if (f.endswith('.csv') or f.endswith('.xlsx')) and not f.startswith('__')]
    df = []
    columns_set = []
    
    for raw_dataset_file in raw_dataset_files:
        raw_dataset_path = os.path.join(raw_dataset_dir, raw_dataset_file)
        try:
            if raw_dataset_file.endswith('.csv'):
                _df = pd.read_csv(raw_dataset_path, dtype=str)
            elif raw_dataset_file.endswith('.xlsx'):
                _df = pd.read_excel(raw_dataset_path, dtype=str)
                
            _df = _df.dropna(thresh=int(_df.shape[1] / 2))
            if not _df.empty:
                columns_set.append(set(_df.columns))
                df.append(_df)
        except Exception as e:
            print(f"Error reading {raw_dataset_path}: {e}")
            
    if columns_set:
        all_columns = set.union(*columns_set)
        common_columns = set.intersection(*columns_set)
        unique_columns = all_columns - common_columns
        if unique_columns:
            print("\nXUẤT HIỆN CÁC CỘT KHÔNG CÙNG FORMAT VỚI CÁC DATASET KHÁC: ", unique_columns, "\n")
    
    # MERGER DATA
    if df:
        df = pd.concat(df, ignore_index=True)
        df.to_csv(merged_dataset_csv, index=False)
    else:
        print("No CSV files found in the specified directory.")
    
    clear_files(processed_dir)
    if split_column:
        split_data(df, split_column=split_column, save_dir = processed_dir)
    else:
        df.to_csv(os.path.join(processed_dir, "no_split.csv"))
    
    dataset_files = [f for f in os.listdir(processed_dir) if f.endswith('.csv')]
    for dataset_file in dataset_files:
        dataset_path = os.path.join(processed_dir, dataset_file)
        name = dataset_file.split(".")[0]
        df, columns_encoder = preprocessing(dataset_path)

        # normalize dataframe
        normalized_df, min_max_scaler = min_max_scale(df)
        print(normalized_df)

        # split data
        X = normalized_df[input_columns]
        y = normalized_df[output_columns]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.1, random_state=42)

        # model = LightGBMModel()
        model = LinearRegressionModel(name=name)
        model.train_all_combinations(
            X_train, y_train, input_columns, output_columns)
        # save model
        save_model(model, model_path)

        # test dataframe
        test = pd.concat([pd.DataFrame(X_test), pd.DataFrame(y_test)], axis=1)
        test_inverse = pd.DataFrame(min_max_scaler.inverse_transform(test),
                                    columns=input_columns + output_columns)
        # test_inverse = test

        # evaluate
        metrics = pd.DataFrame(
            {"Input": [], "Output": [], "MAE": [], "MSE": [], "RMSE": [], "R2": []})
        current_input_columns = input_columns.copy()
        for i, output_column in enumerate([None] + output_columns[:-1]):
            if output_column:
                current_input_columns.append(output_column)
            # predict
            print("================================================================================================")
            y_pred = model.predict(test[current_input_columns])
            current_output_columns = [
                col for col in output_columns if col not in current_input_columns]

            pred = pd.concat([pd.DataFrame(test[current_input_columns]).reset_index(
                drop=True), pd.DataFrame(y_pred).reset_index(drop=True)], axis=1)
            pred.columns = current_input_columns + current_output_columns
            
            pred_inverse = pd.DataFrame(min_max_scaler.inverse_transform(pred),
                                        columns=current_input_columns + current_output_columns)
            

            pred_inverse_csv = os.path.join(pred_path, "pred_{}.csv".format(i))
            pred_inverse.to_csv(pred_inverse_csv, index=False)

            mae, mse, rmse, r2 = evaluate(
                test_inverse[current_output_columns], pred_inverse[current_output_columns])

            print("Average error for {} cases of inputs: {} ==> outputs: {}".format(
                len(test), current_input_columns, current_output_columns))
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
        metrics.to_csv(metrics_csv, index=False)

        # extract json
        model.extract_js(js_model_path, index_js, min_max_scaler, columns_encoder)

    # run notebooks
    # if running_notebooks:
    #     run_notebooks(notebooks_path)


if __name__ == "__main__":
    main()
