import pandas as pd
import numpy as np
import uuid
import json
import joblib
import os
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from xgboost import XGBClassifier, XGBRegressor
from sklearn.metrics import accuracy_score, f1_score, mean_squared_error, r2_score

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
os.makedirs(MODELS_DIR, exist_ok=True)

def train_models(file_path: str, target_column: str, dataset_id: str):
    df = pd.read_csv(file_path)
    
    if target_column not in df.columns:
        raise ValueError(f"Target column {target_column} not found in dataset.")
        
    y = df[target_column]
    X = df.drop(columns=[target_column])
    
    # Auto-detect problem type
    if pd.api.types.is_numeric_dtype(y) and y.nunique() > 10:
        problem_type = "regression"
    else:
        problem_type = "classification"
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    experiment_id = str(uuid.uuid4())
    results = []
    
    if problem_type == "classification":
        models = {
            "Logistic Regression": LogisticRegression(max_iter=1000),
            "Random Forest": RandomForestClassifier(n_estimators=50, random_state=42),
            "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
        }
    else:
        models = {
            "Linear Regression": LinearRegression(),
            "Random Forest": RandomForestRegressor(n_estimators=50, random_state=42),
            "XGBoost": XGBRegressor(random_state=42)
        }
        
    best_model_name = None
    best_model = None
    best_score = -float('inf') if problem_type == "classification" else float('inf')
    best_metrics = {}
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        
        if problem_type == "classification":
            acc = float(accuracy_score(y_test, preds))
            try:
                f1 = float(f1_score(y_test, preds, average='weighted'))
            except:
                f1 = 0.0
            metrics = {"accuracy": acc, "f1": f1}
            score = acc
            if score > best_score:
                best_score = score
                best_model_name = name
                best_model = model
                best_metrics = metrics
        else:
            rmse = float(np.sqrt(mean_squared_error(y_test, preds)))
            r2 = float(r2_score(y_test, preds))
            metrics = {"rmse": rmse, "r2": r2}
            score = rmse
            if score < best_score:  # lower rmse is better
                best_score = score
                best_model_name = name
                best_model = model
                best_metrics = metrics
                
        results.append({
            "model": name,
            "metrics": metrics
        })
        
    # Save best model to disk
    model_path = os.path.join(MODELS_DIR, f"{experiment_id}.pkl")
    joblib.dump(best_model, model_path)
    
    # Save a sample of X_train for SHAP later
    X_train.head(100).to_csv(os.path.join(MODELS_DIR, f"{experiment_id}_X_sample.csv"), index=False)
        
    # Save experiment metadata to JSON
    exp_metadata = {
        "id": experiment_id,
        "dataset_id": dataset_id,
        "target_column": target_column,
        "problem_type": problem_type,
        "best_model_name": best_model_name,
        "metrics": best_metrics,
        "features": list(X.columns)
    }
    with open(os.path.join(MODELS_DIR, f"{experiment_id}_meta.json"), "w") as f:
        json.dump(exp_metadata, f)
    
    return {
        "experiment_id": experiment_id,
        "problem_type": problem_type,
        "best_model": best_model_name,
        "all_results": results
    }
