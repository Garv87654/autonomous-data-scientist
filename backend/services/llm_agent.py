import os
import json
from groq import Groq

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")

def generate_report(experiment_id: str):
    meta_path = os.path.join(MODELS_DIR, f"{experiment_id}_meta.json")
    if not os.path.exists(meta_path):
        return "Experiment not found."
        
    with open(meta_path, "r") as f:
        exp = json.load(f)
        
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        # Mock report if no API key is provided
        return f"""
# Automated Data Science Report

## Executive Summary
This report summarizes the automated machine learning pipeline run on your dataset.

## Target and Problem Type
- **Target Variable**: `{exp['target_column']}`
- **Problem Type**: `{exp['problem_type']}`

## Best Model Selected
After evaluating multiple models, **{exp['best_model_name']}** was chosen as the best performing model based on cross-validation metrics.

## Metrics
{chr(10).join([f'- **{k.upper()}**: {v:.4f}' for k, v in exp['metrics'].items()])}

## Recommendations
1. Deploy this model to production for inference.
2. Consider collecting more data to improve generalization.
3. Conduct further feature engineering based on the SHAP global importance chart.

*(Note: Provide a GROQ_API_KEY in the .env file to generate dynamic, AI-driven reports using Groq.)*
"""

    try:
        client = Groq(api_key=api_key)
        
        prompt = f"""
        Act as an expert data scientist. Generate a professional business report explaining the results of an automated machine learning experiment.
        
        Details:
        - Target Column: {exp['target_column']}
        - Problem Type: {exp['problem_type']}
        - Best Model: {exp['best_model_name']}
        - Metrics: {exp['metrics']}
        - Features Used: {exp['features'][:10]} (showing top 10)
        
        Write an Executive Summary, Model Performance section, and Next Steps. Keep it concise, professional, and accessible to business stakeholders.
        """
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Failed to generate report via API: {str(e)}"
