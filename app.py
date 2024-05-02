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

@app.get("/subject")
def subject():
    data = pd.read_csv('database/subject.csv')
    return data.to_dict(orient='records')

@app.get("/university")
def university():
    data = pd.read_csv('database/university.csv')
    return data.to_dict(orient='records')

@app.get("/relationship")
def relationship():
    mp = pd.read_csv('database/mp.csv')
    subject = pd.read_csv('database/subject.csv')
    university = pd.read_csv('database/university.csv')
    relationship = pd.read_csv('database/relationship.csv')

    merged_df = pd.merge(relationship, mp, left_on='MP', right_on='ID', how='left')
    merged_df = pd.merge(merged_df, subject, left_on='Subject', right_on='ID', how='left')
    merged_df = pd.merge(merged_df, university, left_on='University', right_on='ID', how='left')
    merged_df = merged_df.replace([float('inf'), float('-inf'), float('NaN')], None)
    return merged_df.to_dict(orient='records')
