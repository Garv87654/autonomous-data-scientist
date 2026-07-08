import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# Load env variables (look in backend folder if needed, or root)
load_dotenv(os.path.join(os.path.dirname(__file__), "backend", ".env"))
load_dotenv()

# Import ML logic
from backend.services.data_analyzer import analyze_dataset
from backend.services.cleaner import clean_dataset
from backend.services.eda import generate_eda
from backend.services.model_trainer import train_models
from backend.services.explainer import generate_explanations
from backend.services.llm_agent import generate_report

st.set_page_config(page_title="AI OS for Data", page_icon="🤖", layout="wide")

st.title("🤖 Autonomous Data Scientist Platform")
st.markdown("Upload a dataset and let the AI automatically clean, explore, train, and explain it.")

# Initialize session state
if "df_raw" not in st.session_state:
    st.session_state.df_raw = None
if "df_clean" not in st.session_state:
    st.session_state.df_clean = None
if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "experiment_id" not in st.session_state:
    st.session_state.experiment_id = None
if "dataset_id" not in st.session_state:
    st.session_state.dataset_id = "temp_dataset"
    
TEMP_DIR = "backend/data"
os.makedirs(TEMP_DIR, exist_ok=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["1. Upload & Profile", "2. Clean", "3. EDA", "4. Train", "5. Explain", "6. Report"])

with tab1:
    st.header("Upload Dataset")
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xls", "xlsx"])
    
    if uploaded_file is not None:
        if st.session_state.df_raw is None or st.button("Re-process File"):
            contents = uploaded_file.getvalue()
            analysis_dict, df = analyze_dataset(contents, uploaded_file.name)
            st.session_state.df_raw = df
            st.session_state.analysis = analysis_dict
            
            # Save raw file for backend services
            df.to_csv(os.path.join(TEMP_DIR, f"{st.session_state.dataset_id}.csv"), index=False)
            
        st.success(f"Successfully loaded {uploaded_file.name}")
        
        col1, col2, col3 = st.columns(3)
        stats = st.session_state.analysis["dataset_stats"]
        col1.metric("Rows", stats["row_count"])
        col2.metric("Columns", stats["col_count"])
        col3.metric("Duplicates", stats["duplicate_count"])
        
        st.subheader("Data Quality Issues")
        issues = st.session_state.analysis["quality_issues"]
        if issues:
            for issue in issues:
                st.warning(issue)
        else:
            st.success("No major quality issues detected!")
            
        st.subheader("Inferred Schema")
        schema_df = pd.DataFrame(st.session_state.analysis["schema"])
        st.dataframe(schema_df, use_container_width=True)

with tab2:
    st.header("Auto Cleaning & Preprocessing")
    if st.session_state.df_raw is not None:
        if st.button("Start Auto-Cleaning"):
            with st.spinner("Cleaning dataset..."):
                raw_path = os.path.join(TEMP_DIR, f"{st.session_state.dataset_id}.csv")
                df_clean, logs = clean_dataset(raw_path)
                
                clean_path = os.path.join(TEMP_DIR, f"{st.session_state.dataset_id}_cleaned.csv")
                df_clean.to_csv(clean_path, index=False)
                st.session_state.df_clean = df_clean
                
                st.success("Cleaning complete!")
                for log in logs:
                    st.info(log)
    else:
        st.info("Please upload a dataset first.")

with tab3:
    st.header("Exploratory Data Analysis")
    if st.session_state.df_clean is not None:
        if st.button("Generate EDA"):
            with st.spinner("Analyzing distributions..."):
                clean_path = os.path.join(TEMP_DIR, f"{st.session_state.dataset_id}_cleaned.csv")
                eda_res = generate_eda(clean_path)
                
                st.subheader("Distributions")
                cols = st.columns(2)
                for i, (col_name, dist_data) in enumerate(eda_res["distributions"].items()):
                    with cols[i % 2]:
                        df_dist = pd.DataFrame(dist_data)
                        st.bar_chart(df_dist.set_index("bin"))
                        st.caption(f"Distribution of {col_name}")
    else:
        st.info("Please clean the dataset first.")

with tab4:
    st.header("Train Models")
    if st.session_state.df_clean is not None:
        schema = st.session_state.analysis["schema"]
        target = st.selectbox("Select Target Column", [col["name"] for col in schema])
        
        if st.button("Start AutoML Training"):
            with st.spinner("Training Logistic Regression, Random Forest, and XGBoost..."):
                clean_path = os.path.join(TEMP_DIR, f"{st.session_state.dataset_id}_cleaned.csv")
                results = train_models(clean_path, target, st.session_state.dataset_id)
                st.session_state.experiment_id = results["experiment_id"]
                
                st.success(f"Training Complete! Detected Task: {results['problem_type']}")
                
                for res in results["all_results"]:
                    is_best = res["model"] == results["best_model"]
                    if is_best:
                        st.markdown(f"### 🏆 {res['model']} (Best)")
                    else:
                        st.markdown(f"#### {res['model']}")
                    st.json(res["metrics"])
    else:
        st.info("Please clean the dataset first.")

with tab5:
    st.header("Explainability (SHAP)")
    if st.session_state.experiment_id is not None:
        if st.button("Generate Explanations"):
            with st.spinner("Computing SHAP values..."):
                explanations = generate_explanations(st.session_state.experiment_id)
                if "error" in explanations:
                    st.error(explanations["error"])
                else:
                    st.subheader("Global Feature Importance")
                    df_imp = pd.DataFrame(explanations["global_importance"])
                    st.bar_chart(df_imp.set_index("feature"))
                    
                    st.subheader("Local Explanation (Sample Row)")
                    st.json(explanations["local_explanation_sample"])
    else:
        st.info("Please train a model first.")

with tab6:
    st.header("Executive Report")
    if st.session_state.experiment_id is not None:
        if st.button("Generate AI Report"):
            with st.spinner("Writing report with Groq LLM..."):
                report = generate_report(st.session_state.experiment_id)
                st.markdown(report)
                
                st.download_button(
                    label="Download Markdown",
                    data=report,
                    file_name="ai_data_scientist_report.md",
                    mime="text/markdown"
                )
    else:
        st.info("Please train a model first.")
