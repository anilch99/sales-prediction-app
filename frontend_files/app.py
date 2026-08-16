
import os
import requests
import streamlit as st

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://superkart-backend:7860"
)

st.title("SuperKart Sales Prediction")


left, right = st.columns(2)

with left:
  product_weight = st.number_input("Product Weight", value=12.0)
  product_sugar_content = st.selectbox(
      "Product Sugar Content",
      ["Low Sugar", "Regular", "No Sugar", "reg"]
  )
  product_allocated_area = st.number_input(
      "Product Allocated Area",
      value=0.05
  )

  product_type = st.selectbox(
      "Product Type",
      ["Fruits and Vegetables", "Snack Foods", "Frozen Foods", "Dairy", "Household", "Baking Goods",
       "Canned", "Health and Hygiene", "Meat", "Soft Drinks", "Breads", "Hard Drinks", "Starchy Foods",
       "Breakfast", "Seafood", "Others"]
  )

  product_mrp = st.number_input(
      "Product MRP",
      value=150.0
  )

with right:
  store_id = st.selectbox(
      "Store ID",
      ["OUT001", "OUT002", "OUT003", "OUT004"]
  )

  store_type = st.selectbox(
      "Store Type",
      [
          "Grocery Store",
          "Supermarket Type1",
          "Supermarket Type2",
          "Departmental Store",
          "Food Mart"
      ]
  )

  store_location_city_type = st.selectbox(
      "Store Location City Type",
      [
          "Tier 1",
          "Tier 2",
          "Tier 3"
      ]
  )

  store_size = st.selectbox(
      "Store SIZE",
      ["Medium", "High", "Small"]
  )

  store_age = st.number_input(
      "Store Age",
      value=10
  )


if st.button("Predict Sales"):

    payload = {
        "ProductWeight": product_weight,
        "ProductSugarContent": product_sugar_content,
        "ProductAllocatedArea": product_allocated_area,
        "ProductType": product_type,
        "ProductMRP": product_mrp,

        "StoreId": store_id,
        "StoreType": store_type,
        "StoreSize": store_size,
        "StoreAge": store_age,
        "StoreLocationCityType": store_location_city_type
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
