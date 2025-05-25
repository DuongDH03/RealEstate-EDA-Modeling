import pandas as pd
import numpy as np
import joblib
import pickle
import os
import sys

def debug_prediction(area=100, bedrooms=3, floors=4, district="Đống Đa", 
                    is_main_road=1, is_corner=1, has_car_access=1):
    """
    Debug predictions with the real estate model
    
    Parameters:
    -----------
    area : float
        Area in square meters
    bedrooms : int
        Number of bedrooms
    floors : int
        Number of floors
    district : str
        District name
    is_main_road : int
        Whether the property is on a main road (1=yes, 0=no)
    is_corner : int
        Whether the property is on a corner (1=yes, 0=no)
    has_car_access : int
        Whether the property has car access (1=yes, 0=no)
    """
    print(f"Debugging prediction with parameters:")
    print(f"  Area: {area} m²")
    print(f"  Bedrooms: {bedrooms}")
    print(f"  Floors: {floors}")
    print(f"  District: {district}")
    print(f"  Is on main road: {'Yes' if is_main_road else 'No'}")
    print(f"  Is corner property: {'Yes' if is_corner else 'No'}")
    print(f"  Has car access: {'Yes' if has_car_access else 'No'}")
    
    # Load model features
    try:
        with open('model_features.pkl', 'rb') as f:
            model_features = pickle.load(f)
        print("\nModel features loaded successfully!")
        numeric_features = model_features['numeric_features']
        categorical_features = model_features['categorical_features']
        is_log_transformed = model_features.get('is_log_transformed', False)
        print(f"Numeric features: {numeric_features}")
        print(f"Categorical features: {categorical_features}")
        print(f"Using log transformation: {is_log_transformed}")
    except Exception as e:
        print(f"\nERROR: Could not load model features: {e}")
        return
        
    # Load the trained model
    try:
        # Try loading the XGBoost model first
        model = joblib.load('xgboost_model.joblib')
        model_type = "XGBoost"
        print(f"\n{model_type} model loaded successfully!")
    except Exception as e:
        # Fall back to KNN model
        try:
            model = joblib.load('knn_model.joblib')
            model_type = "KNN"
            print(f"\nXGBoost model not found, using {model_type} model instead: {e}")
        except Exception as e2:
            print(f"\nERROR: Could not load any model: {e2}")
            return
    
    # Prepare input data
    print("\nPreparing input data...")
    
    # Calculate derived features
    bedroom_per_area = bedrooms / area
    
    # Assign district price category (simplified logic)
    affluent_districts = ["Ba Đình", "Hoàn Kiếm", "Tây Hồ", "Cầu Giấy", "Đống Đa", "Hai Bà Trưng"]
    if district in affluent_districts:
        district_price_category = "high_price"
    else:
        district_price_category = "mid_price"
    
    # Create input dataframe
    input_data = {}
    for feature in numeric_features:
        if feature == 'area':
            input_data[feature] = area
        elif feature == 'bedrooms':
            input_data[feature] = bedrooms
        elif feature == 'floors':
            input_data[feature] = floors
        elif feature == 'bedroom_per_area':
            input_data[feature] = bedroom_per_area
        elif feature == 'is_main_road':
            input_data[feature] = is_main_road
        elif feature == 'is_corner':
            input_data[feature] = is_corner
        elif feature == 'has_car_access':
            input_data[feature] = has_car_access
        elif feature == 'address_complete':
            input_data[feature] = 1  # Default value
        else:
            input_data[feature] = 0  # Default for other numeric features
    
    for feature in categorical_features:
        if feature == 'district':
            input_data[feature] = district
        elif feature == 'district_price_category':
            input_data[feature] = district_price_category
        else:
            input_data[feature] = "Unknown"
    
    input_df = pd.DataFrame([input_data])
    print("Input data created:")
    print(input_df)
    
    # Make prediction
    try:
        print("\nMaking prediction...")
        price_prediction = model.predict(input_df)[0]
        
        # Transform prediction back if log-transformed
        if is_log_transformed:
            print(f"Log-transformed prediction: {price_prediction:.4f}")
            price_prediction = np.expm1(price_prediction)
        
        # Calculate price per m2
        price_per_m2 = price_prediction / area
        
        # Print prediction results
        print(f"\nPrediction successful!")
        print(f"Predicted price: {price_prediction:.2f} million VND")
        print(f"Predicted price per m²: {price_per_m2:.2f} million VND/m²")
        
    except Exception as e:
        print(f"\nERROR: Prediction failed: {e}")
        print("Input data that caused the error:")
        print(input_df)

if __name__ == "__main__":
    # Default values
    area = 100
    bedrooms = 3
    floors = 4
    district = "Đống Đa"
    is_main_road = 1
    is_corner = 1
    has_car_access = 1
    
    # Parse command line arguments if provided
    if len(sys.argv) > 1:
        try:
            area = float(sys.argv[1])
            if len(sys.argv) > 2:
                bedrooms = int(sys.argv[2])
            if len(sys.argv) > 3:
                floors = int(sys.argv[3])
            if len(sys.argv) > 4:
                district = sys.argv[4]
            if len(sys.argv) > 5:
                is_main_road = int(sys.argv[5])
            if len(sys.argv) > 6:
                is_corner = int(sys.argv[6])
            if len(sys.argv) > 7:
                has_car_access = int(sys.argv[7])
        except ValueError:
            print("Error parsing arguments. Using default values instead.")
    
    debug_prediction(
        area=area,
        bedrooms=bedrooms,
        floors=floors,
        district=district,
        is_main_road=is_main_road,
        is_corner=is_corner,
        has_car_access=has_car_access
    )
