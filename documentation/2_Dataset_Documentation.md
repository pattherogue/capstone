# Dataset Documentation

## Raw Dataset
The application uses a financial dataset (`data.csv`) containing:

- Income data: User income for the period, representing the total earnings.

- Expense categories: Different categories of expenses, such as rent, groceries, transport, etc.

- Savings goals: User-defined financial goals, such as target savings for a specific period.

- Transaction history: A record of all transactions made, categorized by type (income, expense, etc.).

- User preferences: User-defined settings or preferences for budgeting and financial management.

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
1. Remove invalid entries: Entries with negative amounts or null values are removed or corrected.

2. Standardize category names: Ensure all expense categories have consistent naming conventions (e.g., "Groceries" instead of "grocery").

3. Convert date formats: Dates are standardized to a single format (e.g., YYYY-MM-DD) for consistency.

4. Validate numerical ranges: Ensure values fall within expected ranges (e.g., no income higher than a plausible threshold).

5. Handle missing values: Missing data points are either filled with appropriate values or rows are removed if they are critical.
```

## Data Integrity and Validation
The data cleaning process also involves verifying the integrity and consistency of the dataset:

- Data accuracy checks: Validation steps ensure the correctness of financial data, such as confirming that income is always greater than expenses or checking for reasonable spending distributions.

- Outlier detection: Identifying outlier transactions (e.g., unusually high or low values) to ensure they are legitimate.

## Feature Engineering
To enhance the dataset for analysis and machine learning, several new features are created:

1. Calculated fields:

- Savings ratio: Calculated as (Actual Savings / Income) * 100, showing the percentage of income saved.

- Expense percentages: The proportion of total income spent in each category (e.g., percentage of income spent on groceries).

2. Temporal features:

- Monthly trends: Identifying seasonal spending patterns or recurring expenses over time.

- Seasonal patterns: Detecting periods with higher or lower expenses (e.g., during holidays or special events).

3. Category aggregations:

- Grouping spending by major expense categories such as housing, transportation, and leisure to help users analyze their spending behavior more easily.

4. Statistical features:

- Moving averages: Calculating moving averages over a period to smooth fluctuations in spending and identify underlying trends.

- Variance: Measuring the variance in spending behavior to identify categories with highly fluctuating expenditures.
