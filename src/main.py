from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any

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

@app.post("/upload_pdf/", response_model=DataComparison, responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}})
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file, extract its data, compare with database and return the comparison.

    - **file**: The PDF file to be uploaded
    - **returns**: Data comparison between extracted and database data
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Placeholder for further implementation
    return DataComparison(
        extracted_data={},
        database_data={},
        discrepancies={}
    )
