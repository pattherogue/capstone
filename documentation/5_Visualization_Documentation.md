# Visualization Documentation

## Financial Summary Dashboard
The Financial Summary Dashboard provides an overview of the user's financial status through key metrics and interactive charts:

Key Metrics Display

1. Monthly Income: The total monthly income, displayed as a simple numeric value.

2. Total Expenses: A summary of total expenses categorized by type.

3. Savings Goal: Displays the current savings goal set by the user.

4. Current Savings Ratio: A real-time calculation of the user’s savings ratio, indicating the percentage of income saved after expenses.

Interactive Charts
The following interactive visualizations help users analyze their financial behavior:

### Expense Distribution (Pie Chart)
This pie chart provides a visual breakdown of expenses across different categories:

```javascript
<PieChart>
  <Pie
    data={prepareExpenseData()}
    dataKey="amount"
    nameKey="category"
    cx="50%"
    cy="50%"
    label={(entry) => entry.category}
  />
  <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
  <Legend />
</PieChart>
```
- Purpose: Helps users see the proportion of income spent on each category.

- Interactivity: Tooltips display exact amounts when hovering over the segments.

### Monthly Spending (Bar Chart)
This bar chart visualizes the user’s spending across different categories on a monthly basis:

```javascript
<BarChart data={prepareExpenseData()}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="category" />
  <YAxis />
  <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
  <Bar dataKey="amount" fill="#82ca9d" name="Amount ($)" />
</BarChart>
```
- Purpose: Shows monthly spending trends in a clear and accessible way.

- Interactivity: Tooltips display specific amounts when hovering over the bars.

### Transaction History (Line Chart)
The line chart shows the user's transaction history over time:

```javascript
<LineChart data={transactionData}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="date" />
  <YAxis />
  <Tooltip />
  <Line type="monotone" dataKey="amount" />
</LineChart>
```

- Purpose: Displays fluctuations in income and expenses over a specified time period.

- Interactivity: Users can track transaction trends, helping to identify spending patterns or financial anomalies.


## ML Insights Visualization
In addition to basic financial charts, the application offers advanced visualizations based on machine learning (ML) insights:

1. Model Confidence Indicator: Displays the model’s confidence in the financial recommendations and predictions.

- Purpose: Gives users a sense of how accurate or reliable the insights are.

2. Feature Importance Chart: A bar chart that ranks the features most influential in the model's predictions, such as income, expenses, or savings rate.

- Purpose: Helps users understand which factors impact their financial health the most.

3. Spending Pattern Analysis: A heatmap or other visualization that highlights user spending trends across different categories and time periods.

- Purpose: Identifies high-spending months, seasons, or categories that may require attention.

4. Savings Goal Progress: A progress bar or circular chart that shows the user’s current savings relative to their goal.

- Purpose: Visualizes the user's progress toward meeting their savings objectives.
