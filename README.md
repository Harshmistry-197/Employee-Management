# Employee Management System API

A RESTful backend service built with **FastAPI** and **SQLAlchemy** to manage employee records. This project demonstrates CRUD operations, database integration with MS SQL Server, and robust error handling.

## Features

- **Full CRUD Support**: Create, Read, Update, and Delete employee records.
- **Status Management**: Activate or deactivate employees via PATCH requests.
- **Data Validation**: Strict schema validation using Pydantic (Email format, Salary > 0).
- **ORM Integration**: Database interactions powered by SQLAlchemy and `pyodbc`.
- **Global Error Handling**: Custom exception handlers for 404, 409, and 500 errors.

## Tech Stack

- **Framework**: Python 3.x, FastAPI
- **ORM**: SQLAlchemy
- **Driver**: pyodbc
- **Database**: MS SQL Server
- **Dependency Management**: Poetry

##  Project Structure

```text
employee_managment_system/
├── employee_managment/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db_config.py      # Database engine & session setup
│   │   └── get_db.py         # DB dependency for routes
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── app.py            # API endpoint logic (CRUD)
│   │   ├── base_model.py     # SQLAlchemy models
│   │   └── validation.py     # Pydantic schemas/validation
│   └── __init__.py
├── .env                      # Environment variables (DB Credentials)
├── main.py                   # Application entry point
├── pyproject.toml            # Poetry dependencies
└── README.md
```

## Setup & Installation

1. **Clone the repository**
```
   git clone <repository-url>
   cd employee_managment_system
```
2. **Install Dependencies**
```
poetry install
```
3. **Configure Environment Variables**
```
DATABASE_URL=mssql+pyodbc://<username>:<password>@<server>/<database>?driver=ODBC+Driver+17+for+SQL+Server
```
4. **Run the Application**
```
poetry run uvicorn main:app --reload
```

## API Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/employees` | Fetch all employees |
| **GET** | `/employees/{id}` | Fetch employee by ID |
| **POST** | `/employees` | Create a new employee |
| **PUT** | `/employees/{id}` | Update employee details |
| **PATCH** | `/employees/{id}/status` | Activate / deactivate employee |
| **DELETE** | `/employees/{id}` | Delete an employee |

## Validation & Error Handling
* Email: Must be a valid email format.
* Salary: Must be a float greater than 0.
* 404 Not Found: Returned when an ID does not exist.
* 409 Conflict: Returned if an email already exists in the database.
* 400 Bad Request: Returned for invalid data inputs.
* 500 Internal Server Error: Global handler for unhandled database or server errors.





