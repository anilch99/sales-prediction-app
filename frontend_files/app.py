
import os
import requests
import streamlit as st

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://superkart-backend:7860"
)

st.title("SuperKart Sales Prediction")

product_weight = st.number_input("Product Weight", value=12.0)

product_sugar_content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

product_allocated_area = st.number_input(
    "Product Allocated Area",
    value=0.05
)

product_mrp = st.number_input(
    "Product MRP",
    value=150.0
)

store_size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"]
)

store_location = st.selectbox(
    "Store Location",
    ["Tier 1", "Tier 2", "Tier 3"]
)

store_type = st.selectbox(
    "Store Type",
    [
        "Grocery Store",
        "Supermarket Type1",
        "Supermarket Type2",
        "Supermarket Type3"
    ]
)

product_id_char = st.selectbox(
    "Product ID Category",
    ["FD", "DR", "NC"]
)

store_age = st.number_input(
    "Store Age",
    value=10
)

product_type_category = st.selectbox(
    "Product Type Category",
    ["Perishables", "Non Perishables"]
)

if st.button("Predict Sales"):

    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar_content,
        "Product_Allocated_Area": product_allocated_area,
        "Product_MRP": product_mrp,
        "Store_Size": store_size,
        "Store_Location_City_Type": store_location,
        "Store_Type": store_type,
        "Product_Id_char": product_id_char,
        "Store_Age_Years": store_age,
        "Product_Type_Category": product_type_category
    }

    try:
        response = requests.post(
            f"{BACKEND_URL}/v1/predict",
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            st.success("Prediction completed")
            st.write(result)
        else:
            st.error(response.text)

    except Exception as e:
        st.error(f"Backend connection failed: {e}")
