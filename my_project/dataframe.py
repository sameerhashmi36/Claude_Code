import pandas as pd

# Create a pandas DataFrame with 3 columns and 5 rows
data = {
    'Column1': [1, 2, 3, 4, 5],
    'Column2': ['A', 'B', 'C', 'D', 'E'],
    'Column3': [10.5, 20.3, 15.7, 25.1, 30.9]
}

df = pd.DataFrame(data)

# Display the DataFrame
print("DataFrame with 3 columns and 5 rows:")
print(df)

# Display DataFrame info
print("\nDataFrame Info:")
print(df.info())

# Display DataFrame shape
print(f"\nDataFrame Shape: {df.shape}")
