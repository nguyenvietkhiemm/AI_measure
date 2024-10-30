import os
from sklearn.linear_model import LinearRegression
from tqdm import tqdm
import itertools
import time
import lightgbm as lgb
import pandas as pd
import numpy as np
import json
from datetime import datetime


class LinearRegressionModel:
    def __init__(self, name):
        self.models = []
        self.name = name

    def train_all_combinations(self, X_train, y_train, input_columns, output_columns):
        self.input_columns = input_columns
        self.output_columns = output_columns
        start_time = time.time()
        df = pd.concat([X_train, y_train], axis=1)

        total_combinations = 2 ** len(output_columns)

        # [ALL CASES]
        for combination in tqdm(itertools.product([0, 1], repeat=len(output_columns)), total=total_combinations, desc="Training models"):
            current_input_columns = input_columns.copy()
            for i, val in enumerate(combination):
                if val == 1:
                    current_input_columns.append(output_columns[i])
            current_output_columns = [
                col for col in output_columns if col not in current_input_columns]
            if not current_output_columns:
                continue

            X_train_subset = df[current_input_columns]
            y_train_subset = df[current_output_columns]

            model = LinearRegression()
            model.fit(X_train_subset, y_train_subset)
            self.models.append(model)

        end_time = time.time()
        training_time = end_time - start_time
        print(f"[TRAINING COMPLETED IN {training_time:.2f}S]")

    def predict(self, X_test):
        if not self.models:
            raise Exception("Model has not been trained yet!")

        binary_representation = [1 if col in list(
            X_test.columns) else 0 for col in self.output_columns]

        model_index = int(''.join(map(str, binary_representation)), 2)
        print("MODEL [{}] INPUTS: {}".format(
            model_index, list(X_test.columns)))

        if model_index >= len(self.models):
            raise Exception("No model found for the given input columns!")

        model = self.models[model_index]

        return model.predict(X_test)

    def get_models(self):
        return self.models

    def extract_js(self, js_model_path, original_js_path, min_max_scaler, columns_encoder):
        # Đọc nội dung của file gốc index.js
        try:
            with open(original_js_path, 'r', encoding='utf-8') as file:
                original_js_content = file.read()
        except FileNotFoundError:
            print(f"Error: The file {original_js_path} was not found.")
            return
        except Exception as e:
            print(f"An error occurred while reading {original_js_path}: {e}")
            return
        
            # Thêm thời gian hiện tại
        update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_js = f"// Last updated: {update_time}\n\n"
        
        models_data = []
        min_max_vals = {'min_vals': min_max_scaler.data_min_.astype(np.float32).tolist(),
                        'max_vals': min_max_scaler.data_max_.astype(np.float32).tolist()}
        (min, max) = min_max_scaler.feature_range
        columns_encoder = columns_encoder

        for model in self.models:
            coefficients = model.coef_
            intercept = model.intercept_
            
            weights = [[round(float(w), 3) for w in coef_row] for coef_row in coefficients]
            biases = [round(float(b), 3) for b in intercept]
            # Thêm thông tin mô hình vào danh sách
            models_data.append({
                'w': weights,
                'b': biases,
            })

        min_json = "const min = " + json.dumps(min, separators=(',', ':')) + ";\n"
        max_json = "const max = " + json.dumps(max, separators=(',', ':')) + ";\n"
        model_params_json = "const models = " + json.dumps(models_data, separators=(',', ':')) + ";\n"
        min_max_vals_json = "const min_max_vals = " + json.dumps(min_max_vals, separators=(',', ':')) + ";\n"
        columns_encoder_json = "const columns_encoder = " + json.dumps(columns_encoder, separators=(',', ':')) + ";\n"
        input_columns_json = "const input_columns = " +json.dumps(self.input_columns, separators=(',', ':')) + ";\n"
        output_columns_json = "const output_columns = " +json.dumps(self.output_columns, separators=(',', ':')) + ";\n"
        
        new_js_content = timestamp_js + model_params_json + min_max_vals_json + min_json + max_json + columns_encoder_json + input_columns_json + output_columns_json + original_js_content
        
        try:
            with open("{}\Linear_Model_{}.js".format(js_model_path, self.name), 'w', encoding='utf-8') as json_file:
                json_file.write(new_js_content)
        except Exception as e:
            print(
                f"An error occurred while writing to {js_model_path}: {e}")
            return

        print(f"[IMPORTANT!] Saved the models into {js_model_path}")


class LightGBMModel:
    def __init__(self):
        self.models = []  # Danh sách để lưu các mô hình

    def train(self, X_train, y_train):
        if isinstance(y_train, pd.DataFrame):
            for column in y_train.columns:
                # Chuyển đổi thành mảng một chiều
                y_current = y_train[column].values.ravel()

                # Tạo dataset cho LightGBM
                train_data = lgb.Dataset(X_train, label=y_current)

                # Thiết lập các tham số cho mô hình
                params = {
                    'objective': 'regression',
                    'metric': 'rmse',
                    'boosting_type': 'gbdt',
                    'learning_rate': 0.01,
                    'num_leaves': 31,
                    'max_depth': -1,
                    'verbose': -1,
                }

                # Huấn luyện mô hình
                model = lgb.train(params, train_data, num_boost_round=100)
                self.models.append(model)  # Thêm mô hình vào danh sách
        else:
            raise ValueError(
                "y_train must be a DataFrame with multiple columns.")

    def predict(self, X_test):
        if not self.models:
            raise Exception("Models have not been trained yet!")

        predictions = []
        for model in self.models:
            preds = model.predict(X_test)
            predictions.append(preds)

        # Trả về DataFrame chứa các dự đoán cho từng cột
        return pd.DataFrame(predictions).T

    def get_models(self):
        return self.models
