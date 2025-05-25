"""
Export XGBoost regression model from notebook to a file.
"""
import pandas as pd
import numpy as np
import joblib
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, PowerTransformer, RobustScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import xgboost as xgb
import os
import sys

def main():
    print("Exporting XGBoost model for Streamlit application...")
    
    # Load the preprocessed data
    print("Loading data...")
    df = pd.read_csv('../../Data Preprocessing/alonhadat_processed.csv')
    print(f"Loaded {len(df)} records")
    
    # Define features
    numeric_features = ['area', 'bedrooms', 'floors', 'address_complete', 'bedroom_per_area',
                       'is_main_road', 'is_corner', 'has_car_access']
    categorical_features = ['district', 'district_price_category']
    
    # Create derived features
    print("Creating derived features...")
    df['bedroom_per_area'] = df['bedrooms'] / df['area']
    df['is_corner'] = df['title'].str.contains('GÓC|GÓCH?', case=False, regex=True).astype(int)
    df['is_main_road'] = df['title'].str.contains('MẶT PHỐ|MẶT TIỀN|MẶT ĐƯỜNG', case=False, regex=True).astype(int)
    df['has_car_access'] = df['title'].str.contains('Ô TÔ|OTO|XE HƠI', case=False, regex=True).astype(int)
    
    # Create district price categories
    district_price = df.groupby('district')['price_converted'].median().sort_values()
    price_percentiles = np.percentile(district_price, [33, 66])
    price_labels = ['low_price', 'mid_price', 'high_price']
    district_price_category = pd.cut(district_price, 
                                    bins=[0] + list(price_percentiles) + [float('inf')], 
                                    labels=price_labels)
    district_to_price_category = dict(zip(district_price.index, district_price_category))
    df['district_price_category'] = df['district'].map(district_to_price_category)
    
    # Create log-transformed target
    print("Creating log-transformed target variable...")
    df['price_converted_log'] = np.log1p(df['price_converted'])
    
    # Handle outliers
    print("Removing outliers...")
    # Define IQR outlier removal function
    def remove_outliers_iqr(df, column):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    
    # Apply outlier removal
    df_clean = df.copy()
    for column in ['area', 'price_converted', 'bedrooms', 'floors']:
        df_clean = remove_outliers_iqr(df_clean, column)
    
    print(f"After outlier removal: {len(df_clean)} records ({len(df_clean)/len(df)*100:.2f}% of original data)")
    
    # Update dataset to use cleaned version
    df = df_clean.copy()
    df['price_converted_log'] = np.log1p(df['price_converted'])
    
    # Define features and targets
    X = df[numeric_features + categorical_features].copy()
    y = df['price_converted']
    y_log = df['price_converted_log']
    
    # Split the data
    print("Splitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    _, _, y_train_log, y_test_log = train_test_split(X, y_log, test_size=0.2, random_state=42)
    
    # Create preprocessing pipeline
    print("Creating preprocessing pipeline...")
    numeric_transformer = Pipeline(steps=[
        ('power', PowerTransformer(method='yeo-johnson', standardize=False)),
        ('scaler', RobustScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )
    
    # Define XGBoost parameters
    xgb_params = {
        'n_estimators': 600,
        'max_depth': 6,
        'eta': 0.01,
        'gamma': 1,
        'subsample': 1,
        'colsample_bytree': 0.8,
        'objective': 'reg:squarederror',
        'random_state': 42
    }
    
    # Create and train the log-transformed model
    print("Training XGBoost model with log-transformed target...")
    xgb_model_log = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', xgb.XGBRegressor(**xgb_params))
    ])
    
    xgb_model_log.fit(X_train, y_train_log)
    
    # Save the trained model
    print("Saving model to Application directory...")
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Application'))
    os.makedirs(app_dir, exist_ok=True)
    
    model_path = os.path.join(app_dir, 'xgboost_model.joblib')
    features_path = os.path.join(app_dir, 'model_features.pkl')
    
    joblib.dump(xgb_model_log, model_path)
    
    # Save feature information
    with open(features_path, 'wb') as f:
        pickle.dump({
            'numeric_features': numeric_features,
            'categorical_features': categorical_features,
            'is_log_transformed': True  # Since we're using the log-transformed model
        }, f)
    
    print(f"Model saved to {model_path}")
    print(f"Feature information saved to {features_path}")
    print("Done! The model is ready to use with the Streamlit app.")

if __name__ == "__main__":
    main()
