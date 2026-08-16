
import joblib
import pandas as pd
from flask import Flask, request, jsonify

#Initiate the flasj app
sales_predictor_api = Flask("Sales Predictor")

#load the trained model
saved_model_path = "./superkart_sales_predictions_model_v1_0.joblib"
model = joblib.load(saved_model_path)

#Define a route for the the home page
@sales_predictor_api.get("/")
def home():
    return "Welcom to the Sales Predictor API"

#Define an endpoint o predict the sales price for a single product
@sales_predictor_api.post("/v1/predict")
def predict_price():
  #Get the json data from the request param
  product_info = request.get_json()

  product = {
    "Product_Weight" : 	product_info["ProductWeight"],
    "Product_Sugar_Content" : 	product_info["ProductSugarContent"],
    "Product_Allocated_Area" : 	product_info["ProductAllocatedArea"],
    "Product_Type" : 	product_info["ProductType"],
    "Product_MRP" : 	product_info["ProductMRP"],
    "Store_Id" : 	product_info["StoreId"],
    "Store_Age" : 	product_info["StoreAge"],
    "Store_Size" : 	product_info["StoreSize"],
    "Store_Location_City_Type" : 	product_info["StoreLocationCityType"],
    "Store_Type" : 	product_info["StoreType"]
  }

  input_data = pd.DataFrame([product])

  prediction = model.predict(input_data).tolist()[0]

  return jsonify({'estimataedSalesPrice': prediction})

#Define an endpoint o predict the sales price for a single product
@sales_predictor_api.post("/v1/predictbatch")
def predict_price_batch():
  #get the uploaded CSV file from the request
  file = request.files['file']

  input_data = pd.read_csv(file)

  predictions = [ x for x in model.predict(input_data.drop("Product_Id", axis=1)).tolist() ]

  prod_ID_list = input_data.Product_Id.values().tolist()

  return dict(zip(prod_ID_list, predictions))

#Run the flask app in debug mode
if __name__ == '__main__':
  sales_predictor_api.run(debug=True)

