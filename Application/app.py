import streamlit as st
import pandas as pd
import numpy as np
import re
import joblib
import pickle
from datetime import datetime

# Load the model features
try:
    with open('model_features.pkl', 'rb') as f:
        model_features = pickle.load(f)
    st.sidebar.success("Model features loaded successfully!")
    numeric_features = model_features['numeric_features']
    categorical_features = model_features['categorical_features']
    is_log_transformed = model_features.get('is_log_transformed', False)
except Exception as e:
    st.sidebar.warning(f"Could not load model features: {e}. Using default features.")
    # Default features if model_features.pkl is not found
    numeric_features = ['area', 'bedrooms', 'floors', 'address_complete', 'bedroom_per_area', 
                      'is_main_road', 'is_corner', 'has_car_access']
    categorical_features = ['district', 'district_price_category']
    is_log_transformed = True

# Load the trained model
try:
    # Try loading the XGBoost model first
    model = joblib.load('xgboost_model.joblib')
    model_type = "XGBoost"
    st.sidebar.success(f"{model_type} model loaded successfully!")
except Exception as e:
    # Fall back to KNN model if XGBoost is not available
    try:
        model = joblib.load('knn_model.joblib')
        model_type = "KNN"
        st.sidebar.info(f"XGBoost model not found, using {model_type} model instead.")
    except Exception as e2:
        st.sidebar.error(f"Error loading models: {e2}")
        model = None
        model_type = "None"

# Function to extract district from address
def extract_district(address):
    # Common districts in Hanoi
    districts = [
        "Ba Đình", "Hoàn Kiếm", "Tây Hồ", "Long Biên", "Cầu Giấy", 
        "Đống Đa", "Hai Bà Trưng", "Hoàng Mai", "Thanh Xuân", "Hà Đông", 
        "Bắc Từ Liêm", "Nam Từ Liêm", "Sơn Tây", "Ba Vì", "Chương Mỹ", 
        "Đan Phượng", "Đông Anh", "Gia Lâm", "Hoài Đức", "Mê Linh", 
        "Mỹ Đức", "Phú Xuyên", "Phúc Thọ", "Quốc Oai", "Sóc Sơn", 
        "Thạch Thất", "Thanh Oai", "Thanh Trì", "Thường Tín", "Ứng Hòa"
    ]
    
    # Try to find a district match
    for district in districts:
        if district.lower() in address.lower():
            return district
    
    # Default if no district found
    return "Unknown"

# Function to extract ward category from address
def extract_ward_category(address):
    # Simple logic: categorize by district affluence
    # This is a simplified version - would need to be enhanced with actual data
    affluent_districts = ["Ba Đình", "Hoàn Kiếm", "Tây Hồ", "Cầu Giấy", "Đống Đa", "Hai Bà Trưng"]
    district = extract_district(address)
    
    if district in affluent_districts:
        return "high_price"  # Updated to match model's price category values
    elif district == "Unknown":
        return "mid_price"  # Default category
    else:
        return "low_price"  # Less affluent category

# Function to check if property is on a corner
def is_corner_property(address):
    corner_terms = ["góc", "ngã tư", "giao", "góc"]
    return any(term in address.lower() for term in corner_terms)

# Function to check if property is on a main road
def is_main_road(address):
    main_road_terms = ["mặt phố", "mặt tiền", "mặt đường", "phố chính"]
    return any(term in address.lower() for term in main_road_terms)

# Function to check if property has car access
def has_car_access(address):
    car_terms = ["ô tô", "oto", "xe hơi", "đỗ cửa"]
    return any(term in address.lower() for term in car_terms)

# Main UI
st.title("Real Estate Price Predictor")
st.write("Dự đoán giá bất động sản sử dụng mô hình học máy XGBoost")

with st.form("listing_form"):
    dia_chi = st.text_input("Địa chỉ (VD: Số 1 Đại Cồ Việt, Hai Bà Trưng, Hà Nội)")
    
    col1, col2 = st.columns(2)
    with col1:
        so_phong_ngu = st.number_input("Số phòng ngủ", min_value=1, max_value=10, value=3)
        so_tang = st.number_input("Số tầng", min_value=1, max_value=50, value=4)
    
    with col2:
        dien_tich = st.number_input("Diện tích (m²)", min_value=10, max_value=500, value=100)
        
    advanced = st.expander("Thông tin bổ sung (tùy chọn)")
    with advanced:
        is_corner_manual = st.checkbox("Nhà góc phố", value=False)
        is_main_road_manual = st.checkbox("Mặt đường chính", value=False)
        has_car_access_manual = st.checkbox("Có chỗ để xe ô tô", value=False)
        
    submitted = st.form_submit_button("Dự đoán giá")

if submitted and model:
    try:
        # Convert input to appropriate types
        area = float(dien_tich) 
        bedrooms = int(so_phong_ngu)
        floors = int(so_tang)
        
        # Calculate derived features
        bedroom_per_area = bedrooms / area
        
        # Use manual checkbox values if provided, otherwise infer from address
        is_corner = 1 if is_corner_manual else (1 if is_corner_property(dia_chi) else 0)
        is_main_road_val = 1 if is_main_road_manual else (1 if is_main_road(dia_chi) else 0)
        has_car_access_val = 1 if has_car_access_manual else (1 if has_car_access(dia_chi) else 0)
        
        district = extract_district(dia_chi)
        district_price_category = extract_ward_category(dia_chi)
        
        # Display extracted features for transparency
        st.write("Thông tin đã nhập:")
        st.write({
            "Địa chỉ": dia_chi,
            "Số phòng ngủ": so_phong_ngu,
            "Số tầng": so_tang,
            "Diện tích": dien_tich,
        })
        
        st.write("Đặc điểm được trích xuất:")
        st.write({
            "Vị trí": district,
            "Loại khu vực": district_price_category,
            "Nhà góc": "Có" if is_corner else "Không",
            "Mặt đường chính": "Có" if is_main_road_val else "Không",
            "Đỗ xe ô tô": "Có" if has_car_access_val else "Không",
        })
        
        # Create input dataframe with the required features
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
                input_data[feature] = is_main_road_val
            elif feature == 'is_corner':
                input_data[feature] = is_corner
            elif feature == 'has_car_access':
                input_data[feature] = has_car_access_val
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
                input_data[feature] = "Unknown"  # Default for other categorical features
        
        # Convert to DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Make prediction
        try:
            price_prediction = model.predict(input_df)[0]
            
            # Transform prediction back if log-transformed
            if is_log_transformed:
                price_prediction = np.expm1(price_prediction)
                
            # Calculate price per m2
            price_per_m2 = price_prediction / area
            
            # Format currency as Vietnamese Đồng (millions)
            formatted_price = f"{price_prediction:,.2f} triệu"
            formatted_price_per_m2 = f"{price_per_m2:,.2f} triệu/m²"
            
            # Display prediction results
            st.success(f"Giá dự kiến: {formatted_price} VND")
            st.info(f"Giá dự kiến trên m²: {formatted_price_per_m2}")
            
            # Show model information
            st.info(f"Dự đoán bằng mô hình: {model_type}")
            
        except Exception as pred_error:
            st.error(f"Lỗi khi dự đoán: {pred_error}")
            st.write("Chi tiết đầu vào:")
            st.write(input_df)
        
    except ValueError as e:
        st.error(f"Lỗi định dạng dữ liệu: {e}. Vui lòng kiểm tra lại dữ liệu nhập vào.")
    except Exception as e:
        st.error(f"Lỗi khi dự đoán giá: {e}")
elif submitted and not model:
    st.error("Không thể tải mô hình. Vui lòng kiểm tra lại file mô hình.")

# Add information about the models
with st.sidebar:
    st.title("Thông tin mô hình")
    st.write(f"Mô hình đang sử dụng: **{model_type}**")
    if is_log_transformed:
        st.write("Sử dụng biến đổi log cho giá dự đoán")
    
    st.write("### Đặc điểm mô hình:")
    st.write(f"Đặc điểm số: {', '.join(numeric_features)}")
    st.write(f"Đặc điểm phân loại: {', '.join(categorical_features)}")
    
    st.write("### Hướng dẫn sử dụng:")
    st.write("""
    1. Nhập địa chỉ đầy đủ với tên quận/huyện
    2. Điền số phòng ngủ và số tầng
    3. Nhập diện tích (m²)
    4. Nếu có thông tin chi tiết, mở rộng phần "Thông tin bổ sung"
    5. Nhấn 'Dự đoán giá' để xem kết quả
    """)