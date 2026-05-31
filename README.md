# 🏥 Patient Management API

A lightweight RESTful API built with **FastAPI** to manage patient records stored in a JSON file. Perfect for prototyping, small clinics, or learning FastAPI fundamentals.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📖 Table of Contents

- [Features](#features)
- [Architecture Diagram](#architecture-diagram)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
  - [GET /patients](#get-patients)
  - [GET /patients/{id}](#get-patientsid)
  - [POST /patients](#post-patients)
  - [PUT /patients/{id}](#put-patientsid)
  - [DELETE /patients/{id}](#delete-patientsid)
- [Filtering & Query Parameters](#filtering--query-parameters)
- [Testing](#testing)
- [Data Format](#data-format)
- [Error Handling](#error-handling)
- [Future Improvements](#future-improvements)

## ✨ Features

- **Full CRUD operations** – Create, Read, Update, Delete patient records
- **JSON file storage** – No database setup required, works out‑of‑the‑box
- **Advanced filtering** – By city, gender, age range, and medical history
- **Automatic API documentation** – Interactive Swagger UI at `/docs` and ReDoc at `/redoc`
- **Type validation** – Using Pydantic models
- **Ready‑to‑test** – Included Python test script

## 🏗️ Architecture Diagram

┌─────────────┐      HTTP       ┌─────────────┐     Read/Write     ┌───────────────┐
│   Client    │ ───────────────▶ │  FastAPI    │ ─────────────────▶ │  patients.   
│ (Browser/   │ ◀─────────────── │   Server    │ ◀───────────────── │    json     │
│  Test Script)│      JSON       │  (main.py)  │      JSON          │  (File)      │
└─────────────┘                  └─────────────┘                    └──────────────┘
Alternatively, a more detailed view:


┌─────────────────────────────────────────────────────────────┐
│                         CLIENT SIDE                         │
│  • Test script (test_patients.py)                           │
│  • cURL / Postman                                           │
│  • Web browser (Swagger UI at /docs)                        │
└─────────────────────────────┬───────────────────────────────┘
                              │ HTTP (GET, POST, PUT, DELETE)
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      FASTAPI APPLICATION                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Endpoints:                                           │    │
│  │  • GET    /patients                                  │    │
│  │  • GET    /patients/{id}                            │    │
│  │  • POST   /patients                                  │    │
│  │  • PUT    /patients/{id}                            │    │
│  │  • DELETE /patients/{id}                            │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Business Logic & Validation (Pydantic models)       │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ JSON File Helpers (read_data / write_data)          │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────┬───────────────────────────────┘
                              │ file I/O
                              ▼
                    ┌─────────────────┐
                    │  patients.json  │
                    │  (dictionary of  │
                    │   patient records)│
                    └─────────────────┘
And a data flow diagram (simple steps):


1. Client sends request ──▶ 2. FastAPI validates input
                                    │
                                    ▼
3. FastAPI reads patients.json ──▶ 4. Performs operation (CRUD)
                                    │
                                    ▼
5. Writes back to patients.json ──▶ 6. Returns JSON response to client


📁 Project Structure
text
.
├── main.py                # FastAPI application & JSON helpers
├── patients.json          # Auto‑created data file (ignored in .gitignore)
├── test_patients.py       # Integration test script
├── requirements.txt       # Dependencies
└── README.md              # This file


🚀 Getting Started
Prerequisites
Python 3.8 or higher

pip package manager

Installation
Clone the repository


git clone https://github.com/dotteduniverse/fastapi_patientInfo.git
cd fastapi_patientInfo
Create and activate a virtual environment (recommended)


python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
Install dependencies


pip install fastapi uvicorn requests
Or create a requirements.txt file with:


fastapi>=0.115.0
uvicorn>=0.30.0
requests>=2.31.0
then run:


pip install -r requirements.txt
Running the Server
Start the development server with auto‑reload:


uvicorn main:app --reload --host 0.0.0.0 --port 8000
Now visit:

API → http://localhost:8000

Interactive docs → http://localhost:8000/docs

ReDoc → http://localhost:8000/redoc

📡 API Endpoints
All endpoints return/accept JSON. The id field is required and unique.

GET /patients
Returns a list of all patients. Supports query parameters for filtering (see below).

Response 200 OK


[
  {
    "id": "P001",
    "Name": "John Doe",
    "City": "New York",
    "Age": 30,
    ...
  }
]
GET /patients/{id}
Retrieve a single patient by its id.

Response 200 OK with patient object
Error 404 Not Found – if patient does not exist

POST /patients
Create a new patient. The id must not already exist.

Request Body – full patient object (see Data Format)

Response 201 Created with the created patient
Error 409 Conflict – if ID already exists

PUT /patients/{id}
Update an existing patient. Only fields sent in the request will be updated (partial update).

Request Body – any subset of patient fields
Response 200 OK with the updated patient
Error 404 Not Found – if patient not found

DELETE /patients/{id}
Remove a patient from the data store.

Response 204 No Content
Error 404 Not Found – if patient not found

🔍 Filtering & Query Parameters
The GET /patients endpoint accepts the following optional parameters:

Parameter	Type	Description	Example
city	string	Filter by case‑insensitive city name	?city=New York
gender	string	Filter by gender (male/female/etc.)	?gender=female
min_age	int	Minimum age (inclusive)	?min_age=18
max_age	int	Maximum age (inclusive)	?max_age=65
medical_history	string	Comma‑separated list of conditions (OR)	?medical_history=diabetes,asthma
Example:
GET /patients?city=Los%20Angeles&min_age=40&medical_history=hypertension

🧪 Testing
A ready‑to‑use Python test script is included. It performs:

Creating two patients

Duplicate ID rejection

Fetching all / single patients

Filtering by city, age, and medical history

Updating a patient (partial update)

Deleting a patient

To run the tests:

bash
# Make sure the server is running (in another terminal)
python test_patients.py
Expected output:

text
Creating patient P001...
 OK
...
All tests passed successfully!
📄 Data Format
Each patient object must follow this structure:

json
{
  "id": "P001",
  "Name": "John Doe",
  "City": "New York",
  "Age": 30,
  "Gender": "male",
  "Height": 180,
  "Weight": 75,
  "Blood_Pressure": "120/80",
  "Heart_Rate": 72,
  "Medical_History": ["hypertension", "diabetes"],
  "Verdict": "Improving"
}
Field	Type	Description
id	string (unique)	Primary identifier
Name	string	Full name
City	string	City of residence
Age	integer	Age in years
Gender	string	e.g. "male", "female", "other"
Height	float	Height in cm
Weight	float	Weight in kg
Blood_Pressure	string	e.g. "120/80"
Heart_Rate	integer	Beats per minute
Medical_History	array of strings	List of diagnosed conditions
Verdict	string	Medical outcome/status
❌ Error Handling
The API returns standard HTTP status codes:

Code	Meaning	When
200	OK	Successful GET / PUT
201	Created	Successful POST
204	No Content	Successful DELETE
400	Bad Request	Validation error (auto from FastAPI)
404	Not Found	Invalid patient ID
409	Conflict	Duplicate ID on POST
422	Unprocessable Entity	Invalid request body (auto from Pydantic)
Example error response:

json
{
  "detail": "Patient not found"
}
🔮 Future Improvements
Replace JSON file with a real database (SQLite, PostgreSQL)

Add authentication (JWT / API keys)

Implement pagination for GET /patients

Add more advanced search (full‑text on Name)

Write unit tests using pytest and httpx.AsyncClient

Dockerize the application

Made with ❤️ using FastAPI

