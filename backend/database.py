import os
from sqlalchemy import create_engine, Column, String, Integer, Float, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

DB_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "ai_data_scientist.db")

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(String, primary_key=True, index=True)
    dataset_id = Column(String, index=True)
    target_column = Column(String)
    problem_type = Column(String)  # 'classification' or 'regression'
    best_model_name = Column(String)
    metrics = Column(JSON)  # e.g., {"accuracy": 0.95, "f1": 0.94}
    features = Column(JSON) # list of feature columns
    
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
