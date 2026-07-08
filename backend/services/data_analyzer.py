import pandas as pd
import numpy as np
import io

def analyze_dataset(file_contents: bytes, filename: str):
    # Read file
    if filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(file_contents))
    elif filename.endswith((".xls", ".xlsx")):
        df = pd.read_excel(io.BytesIO(file_contents))
    else:
        raise ValueError("Unsupported file format")

    row_count, col_count = df.shape
    
    # Analyze columns
    columns_info = []
    quality_issues = []
    
    # Missing values
    missing_counts = df.isnull().sum()
    
    # Duplicate rows
    duplicate_count = int(df.duplicated().sum())
    if duplicate_count > 0:
        quality_issues.append(f"Found {duplicate_count} duplicate rows.")
        
    for col in df.columns:
        col_type = str(df[col].dtype)
        missing = int(missing_counts[col])
        missing_pct = round((missing / row_count) * 100, 2) if row_count > 0 else 0
        unique_count = int(df[col].nunique(dropna=True))
        
        inferred_type = "unknown"
        
        # Type inference
        if pd.api.types.is_numeric_dtype(df[col]):
            inferred_type = "numeric"
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            inferred_type = "datetime"
        elif pd.api.types.is_string_dtype(df[col]) or pd.api.types.is_object_dtype(df[col]):
            # If low unique values relative to total, maybe categorical
            if unique_count / max(row_count, 1) < 0.05 or unique_count < 20:
                inferred_type = "categorical"
            else:
                inferred_type = "text"
                
        # Basic quality checks per column
        if missing_pct > 0:
            quality_issues.append(f"Column '{col}' has {missing_pct}% missing values.")
            
        if unique_count == 1:
            quality_issues.append(f"Column '{col}' is constant (only 1 unique value).")
            
        if inferred_type == "categorical" and unique_count > 50:
             quality_issues.append(f"Column '{col}' is categorical but has high cardinality ({unique_count} unique values).")
             
        # Outlier detection for numeric (IQR)
        if inferred_type == "numeric" and row_count > 0:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = int(((df[col] < lower_bound) | (df[col] > upper_bound)).sum())
            if outliers > 0:
                outlier_pct = round((outliers / row_count) * 100, 2)
                quality_issues.append(f"Column '{col}' has {outliers} outliers ({outlier_pct}%).")
                
        columns_info.append({
            "name": col,
            "pandas_type": col_type,
            "inferred_type": inferred_type,
            "missing_count": missing,
            "missing_percent": missing_pct,
            "unique_count": unique_count
        })
        
    return {
        "dataset_stats": {
            "row_count": row_count,
            "col_count": col_count,
            "duplicate_count": duplicate_count
        },
        "schema": columns_info,
        "quality_issues": quality_issues
    }, df
