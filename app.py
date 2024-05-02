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
    df1 = pd.read_csv('database/mp.csv')
    df2 = pd.read_csv('database/subject.csv')
    df3 = pd.read_csv('database/university.csv')
    relationship_df = pd.read_csv('database/relationship.csv')

    merged_df = pd.merge(relationship_df, df1, left_on='MP', right_on='ID', how='left')
    merged_df = pd.merge(merged_df, df2, left_on='Subject', right_on='ID', how='left')
    merged_df = pd.merge(merged_df, df3, left_on='University', right_on='ID', how='left')
    merged_df = merged_df.replace([float('inf'), float('-inf'), float('NaN')], None)    
    merged_df[['lat', 'lng']] = merged_df['UniLocation'].str.split(',', expand=True)
    merged_df['lat'] = pd.to_numeric(merged_df['lat'])
    merged_df['lng'] = pd.to_numeric(merged_df['lng'])
    return merged_df.to_dict(orient='records')
