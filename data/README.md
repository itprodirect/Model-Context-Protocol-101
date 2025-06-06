# Sample Sales Datasets

## sales_data.csv
This CSV contains dummy sales totals for a three-day period.

| Column | Description |
| ------ | --------------------- |
| date   | ISO formatted date |
| sales  | Daily sales amount USD |

Values are small so the file stays lightweight for testing.

## insurance_sales.csv
Synthetic snapshot of anonymized insurance policy sales.

| Column     | Description                                      |
| ---------- | ------------------------------------------------ |
| PolicyID   | Unique policy identifier                         |
| Premium    | Premium paid by the customer in USD              |
| Commission | Commission earned by the agent in USD            |
| LeadSource | Channel where the lead originated (Online, etc.) |
| State      | Two-letter U.S. state abbreviation               |
