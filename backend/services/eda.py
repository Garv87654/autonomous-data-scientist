import pandas as pd
import numpy as np

def generate_eda(file_path: str):
    df = pd.read_csv(file_path)
    
    eda_result = {
        "correlations": [],
        "distributions": {}
    }
    
    # Numeric correlations
    numeric_df = df.select_dtypes(include=[np.number])
    if not numeric_df.empty and len(numeric_df.columns) > 1:
        corr_matrix = numeric_df.corr().round(2).fillna(0)
        # Convert to list of dicts for frontend heatmap
        for i, col1 in enumerate(corr_matrix.columns):
            for j, col2 in enumerate(corr_matrix.columns):
                # only keep upper triangle to avoid duplicates, or keep all for heatmap
                eda_result["correlations"].append({
                    "x": col1,
                    "y": col2,
                    "value": float(corr_matrix.iloc[i, j])
                })
                
    # Distributions for top features
    for col in df.columns[:10]:  # limit to top 10 to save bandwidth
        if pd.api.types.is_numeric_dtype(df[col]):
            # create histogram bins
            counts, bins = np.histogram(df[col].dropna(), bins=10)
            dist_data = [{"bin": f"{round(bins[i], 2)}-{round(bins[i+1], 2)}", "count": int(counts[i])} for i in range(len(counts))]
            eda_result["distributions"][col] = dist_data
        else:
            # value counts for categorical
            val_counts = df[col].value_counts().head(10)
            dist_data = [{"bin": str(k), "count": int(v)} for k, v in val_counts.items()]
            eda_result["distributions"][col] = dist_data
            
    return eda_result
