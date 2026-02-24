from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json


app = FastAPI()


class Patient(BaseModel):                   # Define a Pydantic model for patient data with field annotations and descriptions
    id: Annotated[str, Field(...,description="Unique identifier for the patient", example="P001")]
    name : Annotated[str, Field(..., description="Full name of the patient", example="John Doe")]   
    city : Annotated[str, Field(..., description="City of residence of the patient", example="New York")]
    age : Annotated[int, Field(..., description="Age of the patient", example=30)]
    gender : Annotated[Literal["Male", "Female", "Other"], Field(..., description="Gender of the patient", example="Male")]
    height : Annotated[float, Field(..., gt=0, description="Height of the patient in centimeters", example=175.5)]
    weight : Annotated[float, Field(..., gt=0, description="Weight of the patient in kilograms", example=70.2)]

    @computed_field
    def bmi(self) -> float:                 # Define a computed field to calculate the Body Mass Index (BMI) of the patient
        return round(self.weight / ((self.height / 100) ** 2), 2)

    @computed_field
    def verdict(self) -> str:                 # Define a computed field to determine the health verdict based on the BMI value
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 25:
            return "Normal weight"
        elif 25 <= self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"


class PatientUpdate(BaseModel):                   # Define a Pydantic model for updating patient data with optional fields
    name : Annotated[str, Field(None, description="Full name of the patient", example="John Doe")]   
    city : Annotated[str, Field(None, description="City of residence of the patient", example="New York")]
    age : Annotated[int, Field(None, description="Age of the patient", example=30)]
    gender : Annotated[Literal["Male", "Female", "Other"], Field(None, description="Gender of the patient", example="Male")]
    height : Annotated[float, Field(None, gt=0, description="Height of the patient in centimeters", example=175.5)]
    weight : Annotated[float, Field(None, gt=0, description="Weight of the patient in kilograms", example=70.2)]        



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
def view_patient(patient_id:str = Path(..., description="The ID of the patient to retrieve", example="P001")):  # Load patient 
    #data and search for the patient with the specified ID, returning the patient's information if found, or an error message if not found.
    data = load_data()
    for patient in data["patients"]:
        if patient["id"] == patient_id:
            return patient
    
    raise HTTPException(status_code=404, detail="Patient not found")  # Raise an HTTP exception if the patient is not found


@app.get("/sort")                        # Define an endpoint to sort patients by age
def sort_patients(order: str = Query("asc", description="Sort order: 'asc' for ascending, 'desc' for descending", example="asc")):
    data = load_data()
    patients = data["patients"]
    
    if order == "asc":
        sorted_patients = sorted(patients, key=lambda x: x["age"])
    elif order == "desc":
        sorted_patients = sorted(patients, key=lambda x: x["age"], reverse=True)
    else:
        raise HTTPException(status_code=400, detail="Invalid sort order. Use 'asc' or 'desc'.")
    
    return JSONResponse(content={"patients": sorted_patients}, status_code=200)  # Return the sorted list of patients in the response


@app.post("/add-patient")                     # Define an endpoint to add a new patient record
def add_patient(patient: Patient):
    data = load_data()
    
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    
    data[patient.id] = patient.model_dump()  # Add the new patient to the data dictionary and save it back to the JSON file
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)        
    return JSONResponse(content={"message": "Patient added successfully"}, status_code=201)


@app.put("/update-patient/{patient_id}")          # Define an endpoint to update an existing patient record
def update_patient(patient_id: str = Path(..., description="The ID of the patient to update", example="P001"), patient_update: PatientUpdate = ...):
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    patient_data = data[patient_id]
    
    update_data = patient_update.model_dump(exclude_unset=True)  # Update the patient's information with the provided data
    for key, value in update_data.items():
        patient_data[key] = value
    

    patient_data['id'] = patient_id  # Ensure the patient ID remains unchanged during the update process

    patient_pydantic = Patient(**patient_data)  # Recalculate the computed fields (BMI and verdict) after updating the patient's information

    existing_patient_info = patient_pydantic.model_dump(exclude='id')
    data[patient_id] = existing_patient_info
    

      # Save the updated patient data back to the JSON file
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)
    
    return JSONResponse(content={"message": "Patient updated successfully"}, status_code=200)


@app.delete("/delete-patient/{patient_id}")          # Define an endpoint to delete a patient record
def delete_patient(patient_id: str = Path(..., description="The ID of the patient to delete", example="P001")):
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]  # Remove the patient from the data dictionary and save it back to the JSON file
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)
    
    return JSONResponse(content={"message": "Patient deleted successfully"}, status_code=200)