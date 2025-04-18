import logging
import os
import pyodbc
import requests
import azure.functions as func

PREDICTION_KEY = os.environ["PREDICTION_KEY"]
PREDICTION_URL = os.environ["PREDICTION_URL"]
SQL_CONNECTION_STRING = os.environ["SQL_CONNECTION_STRING"]

app = func.FunctionApp()

def predict_fruit(image_bytes):
    headers = {
        "Prediction-Key": PREDICTION_KEY,
        "Content-Type": "application/octet-stream"
    }
    response = requests.post(PREDICTION_URL, headers=headers, data=image_bytes)
    predictions = response.json().get("predictions", [])
    if predictions:
        top_prediction = max(predictions, key=lambda x: x["probability"])
        return top_prediction["tagName"]  # Custom Vision tag name
    return "Unknown"

def update_database(fruit_type):
    conn = pyodbc.connect(SQL_CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute("""
        MERGE INTO FruitCounts AS target
        USING (SELECT ? AS FruitType) AS source
        ON target.FruitType = source.FruitType
        WHEN MATCHED THEN
            UPDATE SET Count = Count + 1
        WHEN NOT MATCHED THEN
            INSERT (FruitType, Count) VALUES (?, 1);
    """, (fruit_type, fruit_type))
    conn.commit()
    conn.close()

@app.blob_trigger(arg_name="blob", source="EventGrid", path="input/{name}", connection="AzureWebJobsStorage")
def FruitsInc(blob: func.InputStream):
    logging.info(f"Processing blob: {blob.name}")
    image_bytes = blob.read()
    fruit_type = predict_fruit(image_bytes)
    logging.info(f"Classified as: {fruit_type}")
    update_database(fruit_type)
    logging.info("Database updated.")