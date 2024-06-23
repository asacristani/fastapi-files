import os
import csv
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any

from src.pdf_service import PdfService


def read_database():
    """ Read from mock database """
    with open("data/database.csv", mode="r") as infile:
        reader = csv.DictReader(infile)
        data = {rows["Company Name"]: rows for rows in reader}
    return data


app = FastAPI()

class PDFUploadResponse(BaseModel):
    filename: str = Field(..., example="healthinc.pdf")

class DataComparison(BaseModel):
    extracted_data: Dict[str, Any] = Field(..., example={
        "Company Name": "HealthInc",
        "Industry": "Healthcare",
        "Market Capitalization": 3000,
        "Revenue (in millions)": 1000,
        "Equity (in millions)": 666,
        # more fields...
    })
    database_data: Dict[str, Any] = Field(..., example={
        "Company Name": "HealthInc",
        "Industry": "Healthcare",
        "Market Capitalization": 3000,
        "Revenue (in millions)": 1000,
        "Equity (in millions)": 600,
        # more fields...
    })
    discrepancies: Dict[str, Dict[str, Any]] = Field(..., example={
        "Equity (in millions)": {
            "pdf": 666,
            "db": 600
        }
        # more discrepancies...
    })

class ErrorResponse(BaseModel):
    detail: str = Field(..., example="Invalid file type")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/upload_pdf/", response_model=DataComparison, responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}})
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file, extract its data, compare with database and return the comparison.

    - **file**: The PDF file to be uploaded
    - **returns**: Data comparison between extracted and database data
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Write the PDF file
    file_location = f"assets/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    # Extract data from PDF using PdfService
    pdf_service = PdfService(key="TEST_KEY")

    try:
        extracted_data = pdf_service.extract(file_path=file_location)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    

    # Read from DB
    database_data = read_database()
    company_name = extracted_data["Company Name"]

    if company_name not in database_data:
        raise HTTPException(status_code=404, detail="Company not found in database")

    db_data = database_data[company_name]

    # Get discrepancies
    discrepancies = {
        key: {
            "pdf": extracted_data[key],
            "db": db_data.get(key)
        }
        for key in extracted_data if str(extracted_data[key]) != str(db_data.get(key))
    }
    
    # Placeholder for further implementation
    return DataComparison(
        extracted_data=extracted_data,
        database_data=db_data,
        discrepancies=discrepancies
    )
