import os
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from database import engine, Base, get_db
from sqlalchemy.orm import Session

from services.data_analyzer import analyze_dataset
from services.cleaner import clean_dataset
from services.eda import generate_eda
from services.model_trainer import train_models
from services.explainer import generate_explanations
from services.llm_agent import generate_report

app = FastAPI(title="Autonomous Data Scientist API")

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return Response(content=b'', media_type="image/x-icon")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

class TrainRequest(BaseModel):
    dataset_id: str
    target_column: str

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(('.csv', '.xls', '.xlsx')):
        raise HTTPException(status_code=400, detail="Only CSV and Excel supported")
        
    try:
        contents = await file.read()
        dataset_id = str(uuid.uuid4())
        
        # Analyze and save raw file locally
        analysis_result, df = analyze_dataset(contents, file.filename)
        df.to_csv(os.path.join(DATA_DIR, f"{dataset_id}.csv"), index=False)
        
        return {
            "dataset_id": dataset_id,
            "filename": file.filename,
            "analysis": analysis_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/clean/{dataset_id}")
def clean_data(dataset_id: str):
    file_path = os.path.join(DATA_DIR, f"{dataset_id}.csv")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    cleaned_df, cleaning_log = clean_dataset(file_path)
    cleaned_df.to_csv(os.path.join(DATA_DIR, f"{dataset_id}_cleaned.csv"), index=False)
    
    return {"cleaning_log": cleaning_log}

@app.get("/api/eda/{dataset_id}")
def get_eda(dataset_id: str):
    file_path = os.path.join(DATA_DIR, f"{dataset_id}_cleaned.csv")
    if not os.path.exists(file_path):
        # Fallback to raw if not cleaned
        file_path = os.path.join(DATA_DIR, f"{dataset_id}.csv")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Dataset not found")
            
    eda_result = generate_eda(file_path)
    return eda_result

@app.post("/api/train")
def train_model(req: TrainRequest, db: Session = Depends(get_db)):
    file_path = os.path.join(DATA_DIR, f"{req.dataset_id}_cleaned.csv")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Cleaned dataset not found. Please clean first.")
        
    result = train_models(file_path, req.target_column, req.dataset_id, db)
    return result

@app.get("/api/explain/{experiment_id}")
def explain_model(experiment_id: str):
    # Retrieve experiment metadata to know which model/data to load
    # In a real app we'd load the model pickle, but for transparency 
    # we'll run explainer logic inline or mock it if pickling is skipped.
    result = generate_explanations(experiment_id)
    return result

@app.post("/api/report/{experiment_id}")
def get_report(experiment_id: str):
    report_text = generate_report(experiment_id)
    return {"report": report_text}

