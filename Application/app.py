import streamlit as st
import requests

st.title("Demo App")

with st.form("listing_form"):
    muc_gia = st.text_input("Mức giá (VD: 2 tỷ, 10 triệu)")
    muc_gia_internet = st.text_input("Mức giá internet")
    muc_gia_nuoc = st.text_input("Mức giá nước")
    muc_gia_dien = st.text_input("Mức giá điện")
    noi_that = st.selectbox("Nội thất", ["", "Đầy đủ", "Cơ bản", "Không"])
    phap_ly = st.selectbox("Pháp lý", ["", "Sổ đỏ/ Sổ hồng", "Hợp đồng mua bán", "Khác"])
    so_phong_ngu = st.text_input("Số phòng ngủ (VD: 2 phòng)")
    so_phong_tam = st.text_input("Số phòng tắm, vệ sinh (VD: 1 phòng)")
    so_tang = st.text_input("Số tầng (VD: 3 tầng)")
    thoi_gian_vao_o = st.text_input("Thời gian dự kiến vào ở")
    tien_ich = st.text_area("Tiện ích (phân tách bằng dấu phẩy)")
    title = st.text_input("Title")
    duong_vao = st.text_input("Đường vào (VD: 5 m)")

    submitted = st.form_submit_button("Submit")

if submitted:
    st.write("Thông tin đã nhập:")
    st.write({
        "Mức giá": muc_gia,
        "Mức giá internet": muc_gia_internet,
        "Mức giá nước": muc_gia_nuoc,
        "Mức giá điện": muc_gia_dien,
        "Nội thất": noi_that,
        "Pháp lý": phap_ly,
        "Số phòng ngủ": so_phong_ngu,
        "Số phòng tắm, vệ sinh": so_phong_tam,
        "Số tầng": so_tang,
        "Thời gian dự kiến vào ở": thoi_gian_vao_o,
        "Tiện ích": tien_ich,
        "Title": title,
        "Đường vào": duong_vao
    })
    # Prepare data for the ML model
    data = {
        "muc_gia": muc_gia,
        "muc_gia_internet": muc_gia_internet,
        "muc_gia_nuoc": muc_gia_nuoc,
        "muc_gia_dien": muc_gia_dien,
        "noi_that": noi_that,
        "phap_ly": phap_ly,
        "so_phong_ngu": so_phong_ngu,
        "so_phong_tam": so_phong_tam,
        "so_tang": so_tang,
        "thoi_gian_vao_o": thoi_gian_vao_o,
        "tien_ich": tien_ich,
        "title": title,
        "duong_vao": duong_vao
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