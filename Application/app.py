import streamlit as st
import requests
from datetime import datetime

st.title("Demo App")

with st.form("listing_form"):
    dia_chi = st.text_input("Địa chỉ (VD: Số 1 Đại Cồ Việt, Hai Bà Trưng, Hà Nội)")
    so_phong_ngu = st.text_input("Số phòng ngủ (VD: 2)")
    so_phong_tam = st.text_input("Số phòng tắm, vệ sinh (VD: 1)")
    so_tang = st.text_input("Số tầng (VD: 3)")
    dien_tich = st.text_input("Diện tích (Đơn vị m2 - VD: 100)")
    submitted = st.form_submit_button("Submit")

if submitted:
    st.write("Thông tin đã nhập:")
    st.write({
        "Địa chỉ": dia_chi,
        "Số phòng ngủ": so_phong_ngu,
        "Số phòng tắm, vệ sinh": so_phong_tam,
        "Số tầng": so_tang,
        "Diện tích": dien_tich,
    })
    # Prepare data for the ML model
    data = {
        "dia_chi": dia_chi,
        "dien_tich": dien_tich,
        "so_phong_ngu": so_phong_ngu,
        "so_phong_tam": so_phong_tam,
        "so_tang": so_tang,
    }

    # Replace with your actual ML model endpoint
    ml_endpoint = "http://localhost:8000/predict"

    try:
        response = requests.post(ml_endpoint, json=data)
        response.raise_for_status()
        result = response.json()
        predicted_price = result.get("predicted_price")
        st.success(f"Giá dự đoán: {predicted_price:,} VND")
    except Exception as e:
        st.error(f"Lỗi khi gửi dữ liệu tới mô hình: {e}")