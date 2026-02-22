from fastapi import FastAPI, Path, HTTPException, Query
import json


app = FastAPI()

def load_data():                            # Function to load patient data from a JSON file
    with open("patients.json", "r") as f:
        patients = json.load(f)
    return patients
    

@app.get("/")
def read_root():                            # Define the root endpoint that returns a welcome message
    return {"message": "Patient Management System API"}


@app.get("/about")                          # Define an endpoint to provide information about the application
def about():
    return {"data": "This is a simple FastAPI application for managing patient records."}


@app.get("/view-patients")                  # Define an endpoint to view all patients
def view_patients():  
    data = load_data()
    return data

@app.get("/view-patient/{patient_id}")      # Define a path parameter for patient ID 
def view_patient(patient_id:int = Path(..., description="The ID of the patient to retrieve", example=1)):  # Load patient 
    #data and search for the patient with the specified ID, returning the patient's information if found, or an error message if not found.
    data = load_data()
    for patient in data["patients"]:        
        if patient["id"] == patient_id:  
            return patient
    
    raise HTTPException(status_code=404, detail="Patient not found")  # Raise an HTTP exception if the patient is not found


@app.get("/sort")                        # Define an endpoint to sort patients by age
def sort_patients(sort_by: str = Query(..., description="The field to sort patients by", example="age"),
                  order: str = Query(..., description="The order to sort patients (asc or desc)", example="asc")):
    data = load_data()
    if sort_by not in ["age", "name"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    
    sorted_patients = sorted(data["patients"], key=lambda x: x[sort_by], reverse=(order == "desc"))
    return {"patients": sorted_patients}    