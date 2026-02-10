from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from Employee_Management.database import get_db
from sqlalchemy.orm import Session
from Employee_Management.database.config import Employee

app = FastAPI()

class EmployeeBase(BaseModel):
    Name: str = Field(..., max_length=100)
    Email: EmailStr
    Department: Optional[str] = Field(None, max_length=100)
    Salary: float
    PhoneNumber: Optional[str] = Field(None, max_length=20)
    IsActive: bool = True

    class Config:
        from_attributes = True


class EmployeePatch(BaseModel):
    Name: Optional[str] = Field(None, max_length=100)
    Email: Optional[EmailStr] = None
    Department: Optional[str] = Field(None, max_length=100)
    Salary: Optional[float] = None
    PhoneNumber: Optional[str] = Field(None, max_length=20)
    IsActive: Optional[bool] = None

# /employee
@app.get("/employee", response_model=List[EmployeeBase], tags=["Get Employee"])
def get_all_employees(db: Session = Depends(get_db)):
    try:
        employees = db.query(Employee).all()

        if not employees:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No employee records found in the database."
            )
        return employees

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )


# /employee/{id}
@app.get("/employee/{employee_id}", response_model=EmployeeBase, tags=['Get Employee'])
def single_employee(employee_id: int, db: Session = Depends(get_db)):
    try:
        employee = db.query(Employee).filter(Employee.Id == employee_id).first()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No employee Id {employee_id} records found in the database."
            )
        return employee
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching the record: {str(e)}"
        )

#/employee post
@app.post("/employee", response_model=EmployeeBase, tags=["Post Employee"])
def create_employee(employee_data: EmployeeBase, db: Session = Depends(get_db)):
    try:
        existing_email = db.query(Employee).filter(Employee.Email == employee_data.Email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {employee_data.Email} is already registered."
            )
        new_emp = Employee(**employee_data.model_dump())
        db.add(new_emp)
        db.commit()
        db.refresh(new_emp)
        return new_emp

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create employee: {str(e)}"
        )



# /employee/{ID} Put
@app.put("/employee/{emp_id}", response_model=EmployeeBase, tags=["Put Employee"])
def update_employee(emp_id: int, updated_data: EmployeeBase, db: Session = Depends(get_db)):
    try:
        db_employee = db.query(Employee).filter(Employee.Id == emp_id).first()
        if not db_employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {emp_id} not found."
            )
        db_employee.Name = updated_data.Name
        db_employee.Email = updated_data.Email
        db_employee.Department = updated_data.Department
        db_employee.Salary = updated_data.Salary
        db_employee.PhoneNumber = updated_data.PhoneNumber
        db_employee.IsActive = updated_data.IsActive

        db.commit()
        db.refresh(db_employee)
        return db_employee

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Update failed: {str(e)}"
        )

# /employee/{Id}/status
@app.patch("/employees/{emp_id}/status", response_model=EmployeeBase, tags=["Patch Employee"])
def update_employee_status(emp_id: int, is_active: bool, db: Session = Depends(get_db)):
    try:
        db_employee = db.query(Employee).filter(Employee.Id == emp_id).first()

        if not db_employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {emp_id} not found."
            )
        db_employee.IsActive = is_active
        db.commit()
        db.refresh(db_employee)
        return db_employee

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update status: {str(e)}"
        )

# /employee/{Id}
@app.delete("/employees/{emp_id}", tags=["Delete Employee"])
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    try:
        db_employee = db.query(Employee).filter(Employee.Id == emp_id).first()
        if not db_employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {emp_id} not found."
            )
        db.delete(db_employee)
        db.commit()

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Delete failed: {str(e)}"
        )
