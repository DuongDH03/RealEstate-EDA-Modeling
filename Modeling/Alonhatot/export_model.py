"""
Export KNN regression model from notebook to a file.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_regression
import joblib

# Load the preprocessed data
df = pd.read_csv('../../Data Preprocessing/alonhadat_processed.csv')

# Create features that were used in the notebook
df['bedroom_per_area'] = df['bedrooms'] / df['area']
df['is_corner'] = df['title'].str.contains('GÓC|GÓCH?', case=False, regex=True).astype(int)
df['is_main_road'] = df['title'].str.contains('MẶT PHỐ|MẶT TIỀN|MẶT ĐƯỜNG', case=False, regex=True).astype(int)
df['has_car_access'] = df['title'].str.contains('Ô TÔ|OTO|XE HƠI', case=False, regex=True).astype(int)

# Create district price categories
district_price = df.groupby('district')['price_per_m2'].median().sort_values()
price_percentiles = np.percentile(district_price, [33, 66])
price_labels = ['low_price', 'mid_price', 'high_price']

district_price_category = pd.cut(district_price, 
                                bins=[0] + list(price_percentiles) + [float('inf')], 
                                labels=price_labels)
district_to_price_category = dict(zip(district_price.index, district_price_category))
df['district_price_category'] = df['district'].map(district_to_price_category)

# Select features
numeric_features = ['area', 'bedrooms', 'floors', 'bedroom_per_area', 'is_main_road',
                   'is_corner', 'has_car_access']
categorical_features = ['ward_cat']

# Define features and target
X = df[numeric_features + categorical_features].copy()
y = df['price_per_m2']

# Create preprocessing pipelines
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# Combine preprocessing steps
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# Using the best parameters from the notebook
best_knn_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('feature_selection', SelectKBest(f_regression, k='all')),
    ('regressor', KNeighborsRegressor(
        n_neighbors=15,
        weights='distance',
        p=2,
        leaf_size=30
    ))
])

# Train the model on the full dataset
best_knn_pipeline.fit(X, y)

# Save the model to a file
model_path = '../../Application/knn_model.joblib'
joblib.dump(best_knn_pipeline, model_path)

print(f"Model saved to {model_path}")
