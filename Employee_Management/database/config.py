from sqlalchemy import create_engine, Column, Integer, Float, Boolean
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

database_url = "mssql+pyodbc://localhost/harsh?driver=ODBC+Driver+17+for+SQL+Server"

try:
    engine = create_engine(database_url)
    print("Successfully connected to database")

    Base = declarative_base()

    session = sessionmaker(bind=engine)
    print("Successfully Created the Session")

except Exception as e:
    print("Unknown Error Occured ",e)
except ConnectionError as e:
    print("Connection Failed ",e)

class Employee(Base):
    __tablename__ = "employee"
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(VARCHAR(100), nullable=False)
    Email = Column(VARCHAR(255), nullable=False, unique=True)
    Department = Column(VARCHAR(255), nullable=False)
    Salary = Column(Float, nullable=False)
    PhoneNumber = Column(VARCHAR(20), unique=True)
    IsActive = Column(Boolean, nullable=False, default=True)



session = session()
def insert_query():
    # Insert record
    try:
        new_employee = Employee(
            Name="Robert Chen",
            Email="r.chen@tech.com",
            Department="Engineering",
            Salary=95000.00,
            PhoneNumber="555-0987",
            IsActive=True
        )

        session.add(new_employee)
        session.commit()
        print("Employee inserted successfully!")

    except Exception as e:
        print("Error occured ",e)


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


