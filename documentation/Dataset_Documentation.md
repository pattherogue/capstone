# Dataset Documentation

## Raw Dataset
The application uses a financial dataset (`data.csv`) containing:
- Income data
- Expense categories
- Savings goals
- Transaction history
- User preferences

### Data Cleaning Process
```python
# Data cleaning code from train_model.py
def load_and_prepare_data(filepath):
    # Read the CSV file
    df = pd.read_csv(filepath)
    
    # Calculate total expenses
    expense_columns = [
        'Rent', 'Loan_Repayment', 'Insurance', 'Groceries', 
        'Transport', 'Eating_Out', 'Entertainment', 'Utilities', 
        'Healthcare', 'Education', 'Miscellaneous'
    ]
    
    df['Total_Expenses'] = df[expense_columns].sum(axis=1)
    df['Actual_Savings'] = df['Income'] - df['Total_Expenses']
    df['Savings_Ratio'] = (df['Actual_Savings'] / df['Income']) * 100
    
    return df

# Data validation steps
1. Remove invalid entries (negative amounts, null values)
2. Standardize category names
3. Convert date formats
4. Validate numerical ranges
5. Handle missing values
```

## Feature Engineering
- Calculated fields: savings ratio, expense percentages
- Temporal features: monthly trends, seasonal patterns
- Category aggregations: spending by category
- Statistical features: moving averages, variance