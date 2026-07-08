import os
import joblib
import pandas as pd
import shap
import numpy as np

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")

def generate_explanations(experiment_id: str):
    model_path = os.path.join(MODELS_DIR, f"{experiment_id}.pkl")
    sample_path = os.path.join(MODELS_DIR, f"{experiment_id}_X_sample.csv")
    
    if not os.path.exists(model_path) or not os.path.exists(sample_path):
        return {"error": "Model or sample data not found"}
        
    model = joblib.load(model_path)
    X = pd.read_csv(sample_path)
    
    # Explain using TreeExplainer if tree-based, else KernelExplainer
    model_name = type(model).__name__
    
    try:
        if 'RandomForest' in model_name or 'XGB' in model_name:
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X)
        else:
            explainer = shap.LinearExplainer(model, X)
            shap_values = explainer.shap_values(X)
            
        # Get mean absolute SHAP values for global feature importance
        if isinstance(shap_values, list): # Multi-class classification returns list
            shap_values = shap_values[1] # Use positive class for binary, or pick one
            
        mean_abs_shap = np.abs(shap_values).mean(axis=0)
        
        feature_importance = [
            {"feature": col, "importance": float(imp)} 
            for col, imp in zip(X.columns, mean_abs_shap)
        ]
        
        # Sort descending
        feature_importance = sorted(feature_importance, key=lambda x: x["importance"], reverse=True)
        
        # Local explanation for the first row
        first_row_shap = shap_values[0]
        local_explanation = [
            {"feature": col, "contribution": float(val), "actual_value": float(X.iloc[0][col])}
            for col, val in zip(X.columns, first_row_shap)
        ]
        local_explanation = sorted(local_explanation, key=lambda x: abs(x["contribution"]), reverse=True)[:5]
        
        return {
            "global_importance": feature_importance[:10], # top 10
            "local_explanation_sample": local_explanation
        }
    except Exception as e:
        return {"error": f"SHAP explanation failed: {str(e)}"}
