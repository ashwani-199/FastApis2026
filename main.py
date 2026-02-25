from ast import If

from fastapi import FastAPI, Path, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
import json


app = FastAPI()


# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database model
class PatientDatabase(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    city = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    height = Column(Float)        
    weight = Column(Float)
    bmi = Column(Float)
    verdict = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Patient(BaseModel):                   # Define a Pydantic model for patient data with field annotations and descriptions
    patient_id: Annotated[str, Field(...,description="Unique identifier for the patient", example="P001")]
    name : Annotated[str, Field(..., description="Full name of the patient", example="John Doe")]   
    city : Annotated[str, Field(..., description="City of residence of the patient", example="New York")]
    age : Annotated[int, Field(..., description="Age of the patient", example=30)]
    gender : Annotated[Literal["Male", "Female", "Other"], Field(..., description="Gender of the patient", example="Male")]
    height : Annotated[float, Field(..., gt=0, description="Height of the patient in centimeters", example=175.5)]
    weight : Annotated[float, Field(..., gt=0, description="Weight of the patient in kilograms", example=70.2)]

    @computed_field
    def bmi(self) -> float:                 # Define a computed field to calculate the Body Mass Index (BMI) of the patient
        height_in_meters = self.height / 100
        return round(self.weight / (height_in_meters ** 2), 2)

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

class PatientResponse(BaseModel):                   # Define a Pydantic model for the patient response, including all fields from the Patient model and the computed fields
    patient_id: str
    name: str
    city: str
    age: int
    gender: str
    height: float   
    weight: float
    bmi: float
    verdict: str


class PatientUpdate(BaseModel):                   # Define a Pydantic model for updating patient data with optional fields
    name : Annotated[str, Field(None, description="Full name of the patient", example="John Doe")]   
    city : Annotated[str, Field(None, description="City of residence of the patient", example="New York")]
    age : Annotated[int, Field(None, description="Age of the patient", example=30)]
    gender : Annotated[Literal["Male", "Female", "Other"], Field(None, description="Gender of the patient", example="Male")]
    height : Annotated[float, Field(None, gt=0, description="Height of the patient in centimeters", example=175.5)]
    weight : Annotated[float, Field(None, gt=0, description="Weight of the patient in kilograms", example=70.2)]        



# def load_data():                            # Function to load patient data from a JSON file
#     with open("patients.json", "r") as f:
#         patients = json.load(f)
#     return patients
    

@app.get("/")
def read_root():                            # Define the root endpoint that returns a welcome message
    return {"message": "Patient Management System API"}


@app.get("/about")                          # Define an endpoint to provide information about the application
def about():
    return {"data": "This is a simple FastAPI application for managing patient records."}


# @app.get("/view-patients")                  # Define an endpoint to view all patients
# def view_patients(): 
#     pass 
    

# @app.get("/view-patient/{patient_id}")      # Define a path parameter for patient ID 
# def view_patient(patient_id:str = Path(..., description="The ID of the patient to retrieve", example="P001")):  # Load patient 
#     #data and search for the patient with the specified ID, returning the patient's information if found, or an error message if not found.
#     data = load_data()
#     for patient in data["patients"]:
#         if patient["id"] == patient_id:
#             return patient
    
#     raise HTTPException(status_code=404, detail="Patient not found")  # Raise an HTTP exception if the patient is not found


# @app.get("/sort")                        # Define an endpoint to sort patients by age
# def sort_patients(order: str = Query("asc", description="Sort order: 'asc' for ascending, 'desc' for descending", example="asc")):
#     data = load_data()
#     patients = data["patients"]
    
#     if order == "asc":
#         sorted_patients = sorted(patients, key=lambda x: x["age"])
#     elif order == "desc":
#         sorted_patients = sorted(patients, key=lambda x: x["age"], reverse=True)
#     else:
#         raise HTTPException(status_code=400, detail="Invalid sort order. Use 'asc' or 'desc'.")
    
#     return JSONResponse(content={"patients": sorted_patients}, status_code=200)  # Return the sorted list of patients in the response


# @app.post("/add-patient")                     # Define an endpoint to add a new patient record
# def add_patient(patient: Patient):
#     data = load_data()
    
#     if patient.id in data:
#         raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    
#     data[patient.id] = patient.model_dump()  # Add the new patient to the data dictionary and save it back to the JSON file
#     with open("patients.json", "w") as f:
#         json.dump(data, f, indent=4)        
#     return JSONResponse(content={"message": "Patient added successfully"}, status_code=201)


# @app.put("/update-patient/{patient_id}")          # Define an endpoint to update an existing patient record
# def update_patient(patient_id: str = Path(..., description="The ID of the patient to update", example="P001"), patient_update: PatientUpdate = ...):
#     data = load_data()
    
#     if patient_id not in data:
#         raise HTTPException(status_code=404, detail="Patient not found")
    
#     patient_data = data[patient_id]
    
#     update_data = patient_update.model_dump(exclude_unset=True)  # Update the patient's information with the provided data
#     for key, value in update_data.items():
#         patient_data[key] = value
    

#     patient_data['id'] = patient_id  # Ensure the patient ID remains unchanged during the update process

#     patient_pydantic = Patient(**patient_data)  # Recalculate the computed fields (BMI and verdict) after updating the patient's information

#     existing_patient_info = patient_pydantic.model_dump(exclude='id')
#     data[patient_id] = existing_patient_info
    

#       # Save the updated patient data back to the JSON file
#     with open("patients.json", "w") as f:
#         json.dump(data, f, indent=4)
    
#     return JSONResponse(content={"message": "Patient updated successfully"}, status_code=200)


# @app.delete("/delete-patient/{patient_id}")          # Define an endpoint to delete a patient record
# def delete_patient(patient_id: str = Path(..., description="The ID of the patient to delete", example="P001")):
#     data = load_data()
    
#     if patient_id not in data:
#         raise HTTPException(status_code=404, detail="Patient not found")
    
#     del data[patient_id]  # Remove the patient from the data dictionary and save it back to the JSON file
#     with open("patients.json", "w") as f:
#         json.dump(data, f, indent=4)
    
#     return JSONResponse(content={"message": "Patient deleted successfully"}, status_code=200)



@app.post("/create-patient", response_model=PatientResponse)                     # Define an endpoint to add a new patient record
def create_patient(patient: Patient, db: Session = Depends(get_db)):
    db_patient = PatientDatabase(**patient.model_dump())  # Create a new patient record in the database using the provided patient data
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return JSONResponse(content={"message": "Patient created successfully", "patient": patient.model_dump()}, status_code=201)


@app.get("/view-all-patients/", response_model=list[PatientResponse])      # Define an endpoint to view all patient records
def view_all_patients(db: Session = Depends(get_db)):
    patients = db.query(PatientDatabase).all()
    return JSONResponse(content={"patients": [PatientResponse(**patient.__dict__).model_dump() for patient in patients]}, status_code=200)  # Return the list of patients in the response



@app.get("/view-patient/{patient_id}", response_model=PatientResponse)      # Define an endpoint to view a specific patient record by ID
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example="P001"), db: Session = Depends(get_db)):
    patient = db.query(PatientDatabase).filter(PatientDatabase.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    patient_dict = PatientResponse(**patient.__dict__).model_dump()  # Convert the patient record to a dictionary format for the response
    
    return JSONResponse(content={"patient": patient_dict}, status_code=200)  # Return the patient's information in the response

@app.get("/sort-patients/", response_model=list[PatientResponse])                        # Define an endpoint to sort patients by age
def sort_patients(order: str = Query("asc", description="Sort order: 'asc' for ascending, 'desc' for descending", example="asc"), db: Session = Depends(get_db)):
    patients = db.query(PatientDatabase).all()
    
    if order == "asc":
        sorted_patients = sorted(patients, key=lambda x: x.id)
    elif order == "desc":
        sorted_patients = sorted(patients, key=lambda x: x.id, reverse=True)
    else:
        raise HTTPException(status_code=400, detail="Invalid sort order. Use 'asc' or 'desc'.")
    
    return JSONResponse(content={"patients": [PatientResponse(**patient.__dict__).model_dump() for patient in sorted_patients]}, status_code=200)  # Return the sorted list of patients in the response 


@app.put("/update-patient/{patient_id}", response_model=PatientResponse)          # Define an endpoint to update an existing patient record in the database
def update_patient(patient_id: str = Path(..., description="The ID of the patient to update", example="P001"), patient_update: PatientUpdate = ..., db: Session = Depends(get_db)):
    patient = db.query(PatientDatabase).filter(PatientDatabase.patient_id == patient_id).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    update_data = patient_update.model_dump(exclude_unset=True)  # Update the patient's information with the provided data
    for key, value in update_data.items():
        setattr(patient, key, value)
    
    db.commit()  # Commit the changes to the database
    db.refresh(patient)  # Refresh the patient instance to get the updated data
    
    return JSONResponse(content={"message": "Patient updated successfully", "patient": PatientResponse(**patient.__dict__).model_dump()}, status_code=200)  # Return the updated patient's information in the response


@app.delete("/delete-patient/{patient_id}")          # Define an endpoint to delete a patient record from the database
def delete_patient(patient_id: str = Path(..., description="The ID of the patient to delete", example="P001"), db: Session = Depends(get_db)):
    patient = db.query(PatientDatabase).filter(PatientDatabase.patient_id == patient_id).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db.delete(patient)  # Delete the patient record from the database
    db.commit()  # Commit the changes to the database
    
    return JSONResponse(content={"message": "Patient deleted successfully"}, status_code=200)  # Return a success message in the response


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)