
import joblib
import os
import pandas as pd

# Check current directory
print("Current working directory:", os.getcwd())

# Check if model file exists
model_path = 'knn_model.joblib'
print(f"Model file exists: {os.path.exists(model_path)}")

# Try to load the model and examine it
try:
    model = joblib.load(model_path)
    print("Model loaded successfully!")
    print("Model type:", type(model))
    
    # Create sample input data with the same format as your app
    sample_data = pd.DataFrame({
        'area': [100],
        'bedrooms': [2],
        'floors': [3],
        'bedroom_per_area': [0.02],
        'is_main_road': [0],
        'is_corner': [0],
        'has_car_access': [0],
        'ward_cat': ['A']  # Check if this should be a string or numeric value
    })
    
    print("\nSample input data:")
    print(sample_data)
    
    # Try a prediction
    try:
        prediction = model.predict(sample_data)
        print("\nPrediction successful!")
        print("Predicted price per m²:", prediction[0])
    except Exception as e:
        print(f"\nError during prediction: {e}")
        print("This is the error you're seeing in your app")
        
        # Try with ward_cat as numeric if it's currently string
        if isinstance(sample_data['ward_cat'][0], str):
            print("\nTrying with numeric ward_cat...")
            ward_mapping = {'A': 0, 'B': 1, 'C': 2}
            sample_data['ward_cat'] = sample_data['ward_cat'].map(ward_mapping)
            try:
                prediction = model.predict(sample_data)
                print("Prediction successful with numeric ward_cat!")
                print("Predicted price per m²:", prediction[0])
                print("\nFIX: You need to convert ward_cat to numeric in your app")
            except Exception as e:
                print(f"Still error with numeric ward_cat: {e}")
        
except Exception as e:
    print(f"Error loading model: {e}")
