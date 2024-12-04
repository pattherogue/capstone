import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler
import joblib

# Load and prepare the data
def load_and_prepare_data(filepath):
    # Read the CSV file
    df = pd.read_csv(filepath)
    
    # Calculate total expenses
    expense_columns = ['Rent', 'Loan_Repayment', 'Insurance', 'Groceries', 
                      'Transport', 'Eating_Out', 'Entertainment', 'Utilities', 
                      'Healthcare', 'Education', 'Miscellaneous']
    
    df['Total_Expenses'] = df[expense_columns].sum(axis=1)
    
    # Calculate actual savings
    df['Actual_Savings'] = df['Income'] - df['Total_Expenses']
    
    # Calculate savings ratio
    df['Savings_Ratio'] = (df['Actual_Savings'] / df['Income']) * 100
    
    return df

# Create features for the ML model
def create_features(df):
    # Select features for prediction
    feature_columns = ['Income', 'Age', 'Dependents', 'Total_Expenses', 
                      'Rent', 'Loan_Repayment', 'Insurance', 'Groceries',
                      'Transport', 'Eating_Out', 'Entertainment', 'Utilities',
                      'Healthcare', 'Education', 'Miscellaneous']
    
    # Convert categorical columns to numeric
    df_processed = pd.get_dummies(df, columns=['Occupation', 'City_Tier'])
    
    # Select all numeric columns for features
    X = df_processed[feature_columns]
    
    # Target variable: Savings_Ratio
    y = df_processed['Savings_Ratio']
    
    return X, y

# Train the model
def train_model(X, y):
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Decision Tree model
    model = DecisionTreeRegressor(random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Calculate accuracy (R² score)
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)
    
    print(f"Training R² score: {train_score:.4f}")
    print(f"Testing R² score: {test_score:.4f}")
    
    return model, scaler

# Generate savings recommendations
def generate_recommendations(income, expenses, savings_ratio):
    recommendations = []
    
    # Basic recommendations based on savings ratio
    if savings_ratio < 10:
        recommendations.append({
            'type': 'warning',
            'message': 'Your savings rate is below recommended levels. Consider reducing discretionary spending.'
        })
    elif savings_ratio < 20:
        recommendations.append({
            'type': 'info',
            'message': 'Your savings rate is moderate. Look for opportunities to increase savings.'
        })
    else:
        recommendations.append({
            'type': 'success',
            'message': 'Great job! You have a healthy savings rate.'
        })
    
    # Expense-specific recommendations
    monthly_income = income
    if expenses['Eating_Out'] > (monthly_income * 0.15):
        recommendations.append({
            'type': 'suggestion',
            'message': 'Consider reducing eating out expenses to increase savings.'
        })
    
    if expenses['Entertainment'] > (monthly_income * 0.1):
        recommendations.append({
            'type': 'suggestion',
            'message': 'Entertainment expenses could be reduced to meet savings goals.'
        })
    
    return recommendations

def main():
    # Load and prepare data
    df = load_and_prepare_data('data.csv')
    
    # Create features and target
    X, y = create_features(df)
    
    # Train model
    model, scaler = train_model(X, y)
    
    # Save model and scaler
    joblib.dump(model, 'savings_model.joblib')
    joblib.dump(scaler, 'scaler.joblib')
    
    print("Model and scaler saved successfully!")

if __name__ == "__main__":
    main()