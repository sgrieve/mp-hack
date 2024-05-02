from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI(title="MP Hack API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    allow_credentials=True,
)

@app.get("/")
def test():
    return {"API": 'Working'}

@app.get("/mp")
def mp():
    data = pd.read_csv('database/mp.csv')
    return data.to_dict(orient='records')
