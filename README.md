# Patient Management System API

A FastAPI application for managing patient records with automatic BMI calculation and health verdict determination.

## Description

This is a comprehensive FastAPI project that provides a RESTful API for managing patient records. It includes features such as:
- Creating new patient records
- Viewing all patients or specific patients by ID
- Updating existing patient information
- Deleting patient records
- Sorting patients by age
- Automatic BMI calculation and health verdict based on height and weight

The application uses SQLAlchemy for database operations with SQLite, and Pydantic for data validation and serialization.

## Installation

1. Clone or download this repository.

2. Navigate to the project directory:
   ```
   cd FastApis2026
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     myenv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source myenv/bin/activate
     ```

4. Install dependencies (if not already installed):
   ```
   pip install fastapi uvicorn sqlalchemy pydantic
   ```

## Usage

To run the application:

```
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Endpoints

### GET /
Returns a welcome message for the Patient Management System API.

**Response:**
```json
{
  "message": "Patient Management System API"
}
```

### GET /about
Returns information about the application.

**Response:**
```json
{
  "data": "This is a simple FastAPI application for managing patient records."
}
```

### POST /create-patient
Creates a new patient record.

**Request Body:**
```json
{
  "patient_id": "P001",
  "name": "John Doe",
  "city": "New York",
  "age": 30,
  "gender": "Male",
  "height": 175.5,
  "weight": 70.2
}
```

**Response:**
```json
{
  "message": "Patient created successfully",
  "patient": {
    "patient_id": "P001",
    "name": "John Doe",
    "city": "New York",
    "age": 30,
    "gender": "Male",
    "height": 175.5,
    "weight": 70.2,
    "bmi": 22.78,
    "verdict": "Normal weight"
  }
}
```

### GET /view-all-patients/
Retrieves all patient records.

**Response:**
```json
{
  "patients": [
    {
      "patient_id": "P001",
      "name": "John Doe",
      "city": "New York",
      "age": 30,
      "gender": "Male",
      "height": 175.5,
      "weight": 70.2,
      "bmi": 22.78,
      "verdict": "Normal weight"
    }
  ]
}
```

### GET /view-patient/{patient_id}
Retrieves a specific patient record by patient ID.

**Parameters:**
- `patient_id` (path): The unique identifier of the patient (e.g., "P001")

**Response:**
```json
{
  "patient": {
    "patient_id": "P001",
    "name": "John Doe",
    "city": "New York",
    "age": 30,
    "gender": "Male",
    "height": 175.5,
    "weight": 70.2,
    "bmi": 22.78,
    "verdict": "Normal weight"
  }
}
```

### GET /sort-patients/
Retrieves all patients sorted by age.

**Query Parameters:**
- `order` (optional): Sort order - "asc" for ascending (default), "desc" for descending

**Response:**
```json
{
  "patients": [
    {
      "patient_id": "P001",
      "name": "John Doe",
      "city": "New York",
      "age": 30,
      "gender": "Male",
      "height": 175.5,
      "weight": 70.2,
      "bmi": 22.78,
      "verdict": "Normal weight"
    }
  ]
}
```

### PUT /update-patient/{patient_id}
Updates an existing patient record.

**Parameters:**
- `patient_id` (path): The unique identifier of the patient to update

**Request Body:** (only include fields to update)
```json
{
  "name": "Jane Doe",
  "weight": 65.0
}
```

**Response:**
```json
{
  "message": "Patient updated successfully",
  "patient": {
    "patient_id": "P001",
    "name": "Jane Doe",
    "city": "New York",
    "age": 30,
    "gender": "Male",
    "height": 175.5,
    "weight": 65.0,
    "bmi": 21.11,
    "verdict": "Normal weight"
  }
}
```

### DELETE /delete-patient/{patient_id}
Deletes a patient record.

**Parameters:**
- `patient_id` (path): The unique identifier of the patient to delete

**Response:**
```json
{
  "message": "Patient deleted successfully"
}
```

## Interactive API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, you can access it at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`