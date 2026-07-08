import pandas as pd
import numpy as np

np.random.seed(42)
n_samples = 200

data = {
    'CustomerID': range(1, n_samples + 1),
    'Age': np.random.randint(18, 70, n_samples),
    'Annual_Income_k': np.random.normal(60, 15, n_samples),
    'Spending_Score': np.random.randint(1, 100, n_samples),
    'Years_as_Customer': np.random.randint(1, 10, n_samples),
    'Store_Location': np.random.choice(['Urban', 'Suburban', 'Rural'], n_samples),
    'Constant_Column': ['Yes'] * n_samples,  # To trigger constant column drop
    'Purchased_Premium': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]) # Target
}

df = pd.DataFrame(data)

# Introduce some missing values to trigger imputation
df.loc[np.random.choice(df.index, 10, replace=False), 'Age'] = np.nan
df.loc[np.random.choice(df.index, 5, replace=False), 'Store_Location'] = np.nan

# Introduce some outliers in Income
df.loc[0, 'Annual_Income_k'] = 250
df.loc[1, 'Annual_Income_k'] = 300

df.to_csv('sample_customer_data.csv', index=False)
print("Created sample_customer_data.csv")
