# FastAPI Simple Application

A simple FastAPI application demonstrating basic API endpoints.

## Description

This is a basic FastAPI project that provides a simple web API with two endpoints:
- Root endpoint (`/`) that returns a greeting
- About endpoint (`/about`) that provides information about the application

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
   pip install fastapi uvicorn
   ```

## Usage

To run the application:

```
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Endpoints

### GET /
Returns a simple greeting.

**Response:**
```json
{
  "Hello": "World"
}
```

### GET /about
Returns information about the application.

**Response:**
```json
{
  "data": "This is a simple FastAPI application."
}
```

## Interactive API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, you can access it at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`