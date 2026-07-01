from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sklearn.preprocessing import MinMaxScaler
from typing import List, Dict, Any
from sklearn.ensemble import RandomForestClassifier
import yfinance as yf
import torch
import torch.nn as nn
import joblib
import numpy as np
import pandas as pd
import pandas_ta
import sqlite3
from datetime import datetime, time

class StockData(BaseModel):
    stock_features : List[Dict[str, Any]]
    symbol : str  

class Stock1DCNN(torch.nn.Module) :
    def __init__(self, sequence_length) :
        super(Stock1DCNN, self).__init__()
        self.layer1 = torch.nn.Conv1d(in_channels=12, out_channels=64, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm1d(64)
        self.act1 = torch.nn.ReLU()
        self.pool1 = nn.MaxPool1d(kernel_size=2)

        self.dropout = nn.Dropout(p=0.3)

        self.layer2 = nn.Conv1d(in_channels=64, out_channels=32, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm1d(32)
        self.act2 = nn.ReLU()
        self.pool2 = nn.MaxPool1d(kernel_size=2)

        self.flatten = nn.Flatten()

        flattened_size = 32 * (sequence_length // 4)
        self.fc = nn.Linear(in_features=flattened_size, out_features=20)
        self.fc2 = nn.Linear(in_features=20, out_features=2)

    def forward(self, x):

        x = self.layer1(x)
        x = self.bn1(x)
        x = self.act1(x)
        x = self.pool1(x)

        x = self.dropout(x)

        x = self.layer2(x)
        x = self.bn2(x)
        x = self.act2(x)
        x = self.pool2(x)

        x = self.flatten(x)

        x = self.fc(x)
        out = self.fc2(x)

        return out

select_model = 1 # Note that (1 = CNN, 2 = Random_Forest) Please Select model 

if select_model == 1 :
    scaler = joblib.load('stock_scaler.pkl')
    model = Stock1DCNN(sequence_length=7) 
    model.load_state_dict(torch.load('1d_cnn_stock_model.pth'))
    model.eval() 

elif select_model == 2 :
    scaler = joblib.load('rf_scaler.joblib')
    model = joblib.load('rf_model.joblib')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/get-bank-data")
def get_bank_data(symbol : str = "KBANK.BK"): # set default KBANK stock
    hour = 7
    bank_stock = yf.Ticker(symbol)
    df = bank_stock.history(interval='1h', period='3mo')
    df.drop(['Dividends', 'Stock Splits'], axis=1, inplace=True, errors='ignore')

    df.ta.sma(length=20, append=True)
    df.ta.rsi(length=14, append=True)
    df.ta.macd(append=True)
    df.ta.obv(append=True)
    df.ta.vwap(append=True)
    df.dropna(inplace=True)

    feature_columns = [
        'Open', 'High', 'Low', 'Close', 'Volume', 
        'SMA_20', 'RSI_14', 'MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9', 'OBV', 'VWAP_D'
    ]
    df = df[feature_columns]
    df = df.tail(hour)

    df.reset_index(inplace=True)
    
    if 'Datetime' in df.columns:
        df['Datetime'] = df['Datetime'].astype(str)

    data_dict = df.to_dict(orient='records')
    return {
        "status": "success",
        "data": data_dict
    }

@app.post("/predict")
def predict_trend(data: StockData):
    try:
        symbol_name = data.symbol

        df = pd.DataFrame(data.stock_features)
        
        feature_columns = [
        'Open', 'High', 'Low', 'Close', 'Volume', 
        'SMA_20', 'RSI_14', 'MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9', 'OBV', 'VWAP_D'
        ]

        input_data = df[feature_columns].values

        scaled_data = scaler.transform(input_data)

        # Model predict upon your select_model
        if select_model == 1 :
            tensor_data = torch.tensor(scaled_data, dtype=torch.float32).unsqueeze(0).transpose(1, 2)

            with torch.no_grad():
                output = model(tensor_data)
                prediction = torch.argmax(output, dim=1).item()

        elif select_model == 2 :
            prediction = model.predict(scaled_data)[0]

        current_time = datetime.now() # open = [10.00, 11.00, 12.00, 13.00, 14.00, 15.00, 16.00]
        Open_time = [10, 11, 12, 13, 14, 15, 16]

        if current_time.hour in Open_time :
            target_time = time(hour=current_time.hour)
        else :
            target_time = time(hour=Open_time[6])

        status = "Up (Buy!)" if prediction == 1 else "Down (Wait!)"

        # Create Database

        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        target_time_str = target_time.strftime("%H:%M:%S")
        status_val = str(status)

        con = sqlite3.connect("stocks.db")

        cur = con.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS Prediction_value(Stock_Name, Current_Date, Target_Date, Status)")

        dataInsert = (symbol_name, current_time_str, target_time_str, status_val)
        cur.execute("INSERT INTO Prediction_value VALUES(?, ?, ?, ?)", dataInsert)

        con.commit()  # Remember to commit the transaction after executing INSERT.
        con.close()

        return {
            "status": "success",
            "stock" : symbol_name[ : -3],
            "prediction_class": prediction,
            "action": status,
            "timestamp": current_time,
            "target_time": target_time.strftime("%H:%M:%S")
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}