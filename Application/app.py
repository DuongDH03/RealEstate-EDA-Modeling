import streamlit as st
import pandas as pd
import numpy as np
import re
import joblib
from datetime import datetime

# Load the trained KNN model
try:
    model = joblib.load('knn_model.joblib')
    st.sidebar.success("KNN model loaded successfully!")
except Exception as e:
    st.sidebar.error(f"Error loading the model: {e}")
    model = None

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
        return "A"  # Affluent ward
    elif district == "Unknown":
        return "C"  # Default category
    else:
        return "B"  # Middle category

# Function to check if property is on a corner
def is_corner_property(address):
    corner_terms = ["góc", "ngã tư", "giao", "góch"]
    return "giao"K
# any(term in address.lower() for term in corner_terms)

# Function to check if property is on a main road
def is_main_road(address):
    main_road_terms = ["mặt phố", "mặt tiền", "mặt đường", "phố chính"]
    return "mặt phố"
# any(term in address.lower() for term in main_road_terms)

# Function to check if property has car access
def has_car_access(address):
    car_terms = ["ô tô", "oto", "xe hơi", "đỗ cửa"]
    return "oto"
# any(term in address.lower() for term in car_terms)

# Main UI
st.title("Real Estate Price Predictor")

with st.form("listing_form"):
    dia_chi = st.text_input("Địa chỉ (VD: Số 1 Đại Cồ Việt, Hai Bà Trưng, Hà Nội)")
    so_phong_ngu = st.text_input("Số phòng ngủ (VD: 2)")
    so_phong_tam = st.text_input("Số phòng tắm, vệ sinh (VD: 1)")
    so_tang = st.text_input("Số tầng (VD: 3)")
    dien_tich = st.text_input("Diện tích (Đơn vị m2 - VD: 100)")
    submitted = st.form_submit_button("Dự đoán giá")

if submitted and model:
    try:
        # Convert input to appropriate types
        area = float(dien_tich) 
        bedrooms = int(so_phong_ngu)
        floors = int(so_tang)
        
        # Calculate derived features
        bedroom_per_area = bedrooms / area
        is_corner = 1 if is_corner_property(dia_chi) else 0
        is_main_road = 1 if is_main_road(dia_chi) else 0
        has_car_access = 1 if has_car_access(dia_chi) else 0
        ward_cat = extract_ward_category(dia_chi)
        
        # Display extracted features for transparency
        st.write("Thông tin đã nhập:")
        st.write({
            "Địa chỉ": dia_chi,
            "Số phòng ngủ": so_phong_ngu,
            "Số phòng tắm, vệ sinh": so_phong_tam,
            "Số tầng": so_tang,
            "Diện tích": dien_tich,
        })
        
        st.write("Đặc điểm được trích xuất:")
        st.write({
            "Vị trí": extract_district(dia_chi),
            "Loại khu vực": ward_cat,
            "Nhà góc": "Có" if is_corner else "Không",
            "Mặt đường chính": "Có" if is_main_road else "Không",
            "Đỗ xe ô tô": "Có" if has_car_access else "Không",
        })
        
        # Create input dataframe with the required features
        input_data = pd.DataFrame({
            'area': [area],
            'bedrooms': [bedrooms],
            'floors': [floors],
            'bedroom_per_area': [bedroom_per_area],
            'is_main_road': [is_main_road],
            'is_corner': [is_corner],
            'has_car_access': [has_car_access],
            'ward_cat': [ward_cat]
        })
        
        # Make prediction
        price_per_m2 = model.predict(input_data)[0]
        total_price = price_per_m2 * area
        
        # Display prediction results
        st.success(f"Giá dự kiến: {total_price:,.0f} VND")
        st.info(f"Giá dự kiến trên m²: {price_per_m2:,.0f} VND/m²")
        
    except ValueError as e:
        st.error(f"Lỗi định dạng dữ liệu: {e}. Vui lòng kiểm tra lại dữ liệu nhập vào.")
    except Exception as e:
        st.error(f"Lỗi khi dự đoán giá: {e}")
elif submitted and not model:
    st.error("Không thể tải mô hình. Vui lòng kiểm tra lại file mô hình.")