from sklearn.linear_model import LinearRegression
import lightgbm as lgb
import pandas as pd
import numpy as np


class LinearRegressionModel:
    def __init__(self):
        self.model = LinearRegression()

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        if self.model is None:
            raise Exception("Model has not been trained yet!")
        return self.model.predict(X_test)
    def get_model(self):
        return self.model

class LightGBMModel:
    def __init__(self):
        self.models = []  # Danh sách để lưu các mô hình

    def train(self, X_train, y_train):
        if isinstance(y_train, pd.DataFrame):
            for column in y_train.columns:
                y_current = y_train[column].values.ravel()  # Chuyển đổi thành mảng một chiều
                
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
            raise ValueError("y_train must be a DataFrame with multiple columns.")

    def predict(self, X_test):
        if not self.models:
            raise Exception("Models have not been trained yet!")
        
        predictions = []
        for model in self.models:
            preds = model.predict(X_test)
            predictions.append(preds)

        return pd.DataFrame(predictions).T  # Trả về DataFrame chứa các dự đoán cho từng cột
    
    def get_models(self):
        return self.models