# 🤖 Autonomous Data Scientist Platform (AI OS)

An end-to-end "AI OS for Data" that automatically acts like a junior data scientist. It ingests generic tabular datasets (CSV/Excel), cleans the data, performs Exploratory Data Analysis (EDA), trains machine learning models, generates SHAP explainability charts, and writes an executive business report using a Large Language Model (Groq/LLaMA 3).

## Features
- **Data Profiling**: Automatically infers column types (numeric, categorical, datetime, text) and identifies data quality issues (missing values, duplicates, outliers, constant columns).
- **Auto Cleaning**: Automatically imputes missing values, drops useless columns, scales numeric data, and encodes categorical data.
- **Automated EDA**: Generates interactive distribution charts and correlations.
- **AutoML Training**: Auto-detects Classification vs. Regression based on the target column. Trains and evaluates Logistic/Linear Regression, Random Forest, and XGBoost models using cross-validation.
- **Explainable AI (XAI)**: Integrates SHAP (SHapley Additive exPlanations) to eliminate the "black box" effect by providing global feature importance and local row-level prediction contributions.
- **Generative AI Reporting**: Uses the Groq API (LLaMA 3 70B) to translate mathematical metrics and SHAP values into a plain-English executive summary.

## Tech Stack
- **Frontend & Backend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-Learn, XGBoost
- **Explainability**: SHAP
- **Generative AI**: Groq API (LLaMA 3)

## How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Garv87654/autonomous-data-scientist.git
   cd autonomous-data-scientist
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables:**
   Create a `.env` file in the root directory and add your Groq API key (required for the AI report generation):
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```
   The app will open automatically in your browser at `http://localhost:8501`.

## Deployment
This project is fully compatible with **Streamlit Community Cloud**. Simply connect your GitHub repository and set the `GROQ_API_KEY` in the Streamlit secrets manager.
