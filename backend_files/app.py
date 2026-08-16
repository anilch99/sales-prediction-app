
import joblib
import pandas as pd
from flask import Flask, request, jsonify

#Initiate the flasj app
sales_predictor_api = Flask("Sales Predictor")

#load the trained model
saved_model_path = "././superkart_sales_predictions_model_v1_0.joblib"
model = joblib.load(saved_model_path)

#Define a route for the the home page
@sales_predictor_api.get("/")
def home():
    return "Welcom to the Sales Predictor API"

#Define an endpoint o predict the sales price for a single product
@sales_predictor_api.post("/v1/product")
def predict_price():
  #Get the json data from the request param
  product_info = request.get_json()

  product = {
    "ProductWeight" : 	product_info["ProductWeight"],
    "ProductSugarContent" : 	product_info["ProductSugarContent"],
    "ProductAllocatedArea" : 	product_info["ProductAllocatedArea"],
    "ProductType" : 	product_info["ProductType"],
    "ProductMRP" : 	product_info["ProductMRP"],
    "StoreId" : 	product_info["StoreId"],
    "StoreEstablishmentYear" : 	product_info["StoreEstablishmentYear"],
    "StoreSize" : 	product_info["StoreSize"],
    "StoreLocationCityType" : 	product_info["StoreLocationCityType"],
    "StoreType" : 	product_info["StoreType"]
  }

  input_data = pd.DataFrame([product])

  prediction = model.predict(input_data).tolist()[0]

  return jsonify({'estimataedSalesPrice': prediction})

#Define an endpoint o predict the sales price for a single product
@sales_predictor_api.post("/v1/productbatch")
def predict_price_batch():
  #get the uploaded CSV file from the request
  file = request.files['file']

  input_data = pd.read_csv(file)

  predictions = [ x for x in model.predict(input_data.drop("Product_Id", axis=1)).tolist() ]

  prod_ID_list = input_data.Product_Id.values().tolist()

  return dict(zip(prod_ID_list, predictions))

#Run the flask app in debug mode
if __name__ == '__main__':
  app.run(debug=True)

