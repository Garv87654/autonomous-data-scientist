import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def clean_dataset(file_path: str):
    df = pd.read_csv(file_path)
    log = []
    
    # Missing values imputation
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if pd.api.types.is_numeric_dtype(df[col]):
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                log.append(f"Imputed missing values in numeric column '{col}' with median ({median_val}).")
            else:
                mode_val = df[col].mode()[0]
                df[col] = df[col].fillna(mode_val)
                log.append(f"Imputed missing values in categorical/text column '{col}' with mode ('{mode_val}').")
                
    # Duplicates
    initial_len = len(df)
    df = df.drop_duplicates()
    if len(df) < initial_len:
        log.append(f"Dropped {initial_len - len(df)} duplicate rows.")
        
    # Constant columns
    cols_to_drop = [col for col in df.columns if df[col].nunique() <= 1]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
        log.append(f"Dropped constant columns: {', '.join(cols_to_drop)}.")
        
    # Scale numeric columns (StandardScaler)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        scaler = StandardScaler()
        # Ensure we don't scale binary columns unnecessarily
        cols_to_scale = [c for c in numeric_cols if df[c].nunique() > 2]
        if cols_to_scale:
            df[cols_to_scale] = scaler.fit_transform(df[cols_to_scale])
            log.append(f"Standardized numeric columns: {', '.join(cols_to_scale)}.")
            
    # Simple label encoding for strings to make them ML ready (for XGBoost / Trees)
    # Ideally we'd use OneHot for low card, but label encoding is easier for a transparent baseline
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in cat_cols:
        df[col] = df[col].astype('category').cat.codes
        log.append(f"Label encoded categorical column '{col}'.")
        
    return df, log
