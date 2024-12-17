"# Personal-budget-tracker-and-currency-converter" 

This is a simple Expense Tracker Application using Tkinter, CustomTkinter, PIL (Pillow), Matplotlib and MySQL. This app helps you keep an eye on how much you spend every day, categorize it, and also see your expenses trend over time. It also offers currency conversion features to optimize how users manage their expenditures in various currencies.

Key features:

1. Expense Management:

The users would be able to add expenses along with title, category (Examples: Housing, Food, Healthcare), amount, and date. The app stores the expenses in MySQL database and the data persists even after closing the application. It shows total expenses and monthly expenses at the mainwindow giving you an overview of your spending as the use of the software goeson.

2. Expense Log:

Users can view a detailed log of all their expenses over a custom date range. The expense log is displayed in a table with columns for Title, Date, Category, and Amount, and the total expenses for the selected period are summarized.

3. Expense Visualization:

User can view their expenses visually using a bar graph to get a better understanding of their spending patterns.This is generated dynamically based on data in the MySQL database and displayed using Matplotlib.

4. Currency Conversion:
The app integrates with an API (ExchangeRate-API) to allow users to convert amounts between different currencies (e.g., USD to INR, EUR to GBP).
