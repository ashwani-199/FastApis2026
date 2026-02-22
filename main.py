from fastapi import FastAPI
import json


app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        patients = json.load(f)
    return patients
    

@app.get("/")
def read_root():
    return {"message": "Patient Management System API"}


@app.get("/about")
def about():
    return {"data": "This is a simple FastAPI application for managing patient records."}


@app.get("/view-patients")
def view_patients():
    data = load_data()
    return data