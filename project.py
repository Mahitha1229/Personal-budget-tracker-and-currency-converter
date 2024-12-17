import tkinter as tk
from PIL import Image, ImageTk
import customtkinter as ctk
import mysql.connector
import validators
from tkinter import messagebox
import tkcalendar
from datetime import datetime, timedelta
from tkinter import ttk
import matplotlib.pyplot as plt
import warnings
import os
import requests
tk.Tk.report_callback_exception=lambda *args: None

class ExpenseTracerApp:
    def __init__(self):
        self.landing_window = ctk.CTk()
        self.landing_window.geometry("850x575")
        self.landing_window.title("Expense Tracker | Home")
        self.landing_window.resizable(False, False)
        self.connection = mysql.connector.connect(
            host="localhost", user="root", password="mysql", database="expense_tracker")  # Fixed the 'user' parameter
        self.create_expenses_table()

        # Create side panel
        self.create_side_panel()

        # Initially show main window
        self.main_window()

    def create_side_panel(self):
        # Side panel frame
        self.side_panel = ctk.CTkFrame(self.landing_window, width=150, height=550)
        self.side_panel.place(x=0, y=0)

        # Side panel buttons
        buttons = [
            ("Home", self.main_window),
            ("Add Expense", self.add_expense),
            ("Visualize Expenses", self.visualize_expense_bar),
            ("Expense Log", self.show_expense_log),
            ("Currency Conversion",self.currency_conversion_window),
        ]

        for i, (text, command) in enumerate(buttons):
            btn = ctk.CTkButton(
                self.side_panel, 
                text=text, 
                command=command, 
                width=140
            )
            btn.place(x=4, y=90 + i*50)

    def create_expenses_table(self):
        cursor = self.connection.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS expenses (
            expense_title_entry VARCHAR(255),
            date_added DATE,
            expense_category VARCHAR(20),
            expense_amount INT
        )
        """
        cursor.execute(query)
        self.connection.commit()

    def main_window(self):
        # Destroy existing frame
        if hasattr(self, 'main_window_frame'):
            self.main_window_frame.destroy()

        self.main_window_frame = ctk.CTkFrame(
            self.landing_window, height=550, width=700)
        self.main_window_frame.place(x=150, y=0)

        # Home Label
        home_label = ctk.CTkLabel(
            self.main_window_frame, text="Home", font=("sans serif", 24, "bold"))
        home_label.place(x=300, y=50)

        # Add Image 
        image_path = r"C:\Users\Mahitha\OneDrive\Desktop\Projects\home_image.png"  # Replace with the correct path to your image

        try:
            image = Image.open(image_path)
            image_resized = image.resize((500, 500))  
            ctk_image = ctk.CTkImage(image_resized, size=(350, 350))
            image_label = ctk.CTkLabel(self.main_window_frame, image=ctk_image, text="") 
            image_label.place(x=100, y=200)
        except Exception as e:
            print(f"Error loading image: {e}")

        # Expense Summary Calculation
        current_date = datetime.now()
        first_day = current_date.replace(day=1)
        next_month = (current_date.replace(day=28) + timedelta(days=4)).replace(day=1)
        last_day = next_month - timedelta(days=1)
        first_day = first_day.strftime("%Y-%m-%d")
        last_day = last_day.strftime("%Y-%m-%d")
        
        try:
            cursor = self.connection.cursor()
            query_to_find_total_expense = "SELECT SUM(expense_amount) FROM expenses;"
            query_to_find_expense_this_month = f"SELECT SUM(expense_amount) FROM expenses WHERE date_added BETWEEN '{first_day}' AND '{last_day}';"
            
            cursor.execute(query_to_find_total_expense)
            total_expense_all_time = cursor.fetchone()
            
            cursor.execute(query_to_find_expense_this_month)
            expense_this_month = cursor.fetchone()
            
            if total_expense_all_time[0] is not None and expense_this_month[0] is not None:
                total_expense_all_time_label = ctk.CTkLabel(
                    self.main_window_frame, 
                    text=f"Total Expense Recorded: {total_expense_all_time[0]}", 
                    font=("sans serif", 18, "bold"))
                total_expense_all_time_label.place(x=200, y=100)
                
                expense_this_month_label = ctk.CTkLabel(
                    self.main_window_frame, 
                    text=f"Total Expense This Month: {expense_this_month[0]}", 
                    font=("sans serif", 18, "bold"))
                expense_this_month_label.place(x=200, y=130)
            else:
                info_label = ctk.CTkLabel(
                    self.main_window_frame, 
                    text="Add Expenses to See Expense Summary", 
                    font=("sans serif", 18))
                info_label.place(x=200, y=100)
        
        except Exception as e:
            info_label = ctk.CTkLabel(
                self.main_window_frame, 
                text="Error Retrieving Expense Data", 
                font=("sans serif", 18))
            info_label.place(x=250, y=100)

    def add_expense(self):
        # Destroy existing frame
        if hasattr(self, 'main_window_frame'):
            self.main_window_frame.destroy()

        self.landing_window.title("Expense Tracker | Add Expense")
        self.main_window_frame = ctk.CTkFrame(
            self.landing_window, height=550, width=750)
        self.main_window_frame.place(x=150, y=0)
        
        # Add Expense Label
        add_expense_label = ctk.CTkLabel(
            self.main_window_frame, text="Add Expense", font=("Futura", 24, 'bold'))
        add_expense_label.place(x=300, y=40)
        
        # Expense Title
        expense_title_label = ctk.CTkLabel(
            self.main_window_frame, text="Expense Title", font=("Futura", 18))
        expense_title_label.place(x=40, y=100)
        expense_title_entry = ctk.CTkEntry(
            self.main_window_frame, placeholder_text="Expense Title", width=160, corner_radius=5, height=10)
        expense_title_entry.place(x=200, y=100)
        
        # Date Selection
        select_date_label = ctk.CTkLabel(self.main_window_frame, text="Select Date", font=("Futura", 18), anchor="w")
        select_date_label.place(x=40, y=150)
        date_picker = tkcalendar.DateEntry(self.main_window_frame, width=16, font=("Helvetica", 14))
        date_picker.place(x=250, y=190)
        
        # Expense Category
        select_expense_category_label = ctk.CTkLabel(
            self.main_window_frame, text="Select Category", font=("Futura", 18))
        select_expense_category_label.place(x=40, y=200)
        expense_category_dropdown = ctk.CTkComboBox(
            self.main_window_frame, width=160, values=["Housing", "Education", "Insurance", "Food", "Transportation", "Healthcare", "Entertainment", "Other"], state="readonly")
        expense_category_dropdown.set("Housing")
        expense_category_dropdown.place(x=200, y=200)
        
        # Expense Amount
        expense_amount_label = ctk.CTkLabel(
            self.main_window_frame, text="Expense Amount", font=("Futura", 18))
        expense_amount_label.place(x=40, y=250)
        expense_amount_entry = ctk.CTkEntry(
            self.main_window_frame, placeholder_text="Expense Amount", width=160, corner_radius=5, height=10)
        expense_amount_entry.place(x=200, y=250)
        
        # Submit Expense Details
        def submit_expense_details():
            expense_title = expense_title_entry.get()
            date_of_expense_added = str(date_picker.get_date())
            expense_category = expense_category_dropdown.get()
            expense_amount = expense_amount_entry.get()

            users_entry = (expense_title, date_of_expense_added,
                           expense_category, expense_amount)
            
            # Check if input fields are empty
            def isEmpty(data):
                return len(data)
            
            result = list(map(isEmpty, users_entry))
            
            try:
                if 0 in result:
                    messagebox.showerror(
                        "Required", "All Input fields are required")
                else:
                    expense_amount = int(expense_amount)
                    query = f'INSERT INTO expenses VALUES ("{expense_title}","{date_of_expense_added}","{expense_category}","{expense_amount}");'
                    cursor = self.connection.cursor()
                    cursor.execute(query)
                    self.connection.commit()
                    messagebox.showinfo(
                        "Success", "Record Inserted Successfully!")
                    expense_title_entry.delete(0, ctk.END)
                    expense_amount_entry.delete(0, ctk.END)

            except ValueError:
                messagebox.showerror(
                    "Error", "Number is expected in amount field")
                expense_amount_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Error while inserting data into database: {str(e)}")
        
        submit_expense_details_button = ctk.CTkButton(
            self.main_window_frame, text="Add", width=160, command=submit_expense_details, font=("Futura", 18))
        submit_expense_details_button.place(x=200, y=300)

    def visualize_expense_bar(self):
        os.makedirs("charts",exist_ok=True)
        plt.savefig("charts/expense_bar_chart.png");
        # Destroy existing frame
        if hasattr(self, 'main_window_frame'):
            self.main_window_frame.destroy()

        warnings.filterwarnings("ignore")
        self.landing_window.title("Expense Tracker | Visualize Expense")
        self.main_window_frame = ctk.CTkFrame(
            self.landing_window, height=550, width=700)
        self.main_window_frame.place(x=150, y=0)

        categories = ["Housing", "Education", "Insurance", "Food", "Transportation", "Healthcare", "Entertainment", "Other"]
        cursor = self.connection.cursor()
        expenses = []
        
        # Queries for each category
        category_queries = {
            "Housing": "SELECT SUM(expense_amount) FROM expenses WHERE expense_category='Housing';",
            "Education": "SELECT SUM(expense_amount) FROM expenses WHERE expense_category='Education';",
            "Insurance": "SELECT SUM(expense_amount) FROM expenses WHERE expense_category='Insurance';",
            "Food": "SELECT SUM(expense_amount) FROM expenses WHERE expense_category='Food';",
            "Transportation": "SELECT SUM(expense_amount) FROM expenses WHERE expense_category='Transportation';",
            "Healthcare": "SELECT SUM(expense_amount) FROM expenses WHERE expense_category='Healthcare';",
            "Entertainment": "SELECT SUM(expense_amount) FROM expenses WHERE expense_category='Entertainment';",
            "Other": "SELECT SUM(expense_amount) FROM expenses WHERE expense_category='Other';"
        }
        
        expenses = []
        for category in categories:
            cursor.execute(category_queries[category])
            expense = cursor.fetchone()[0]
            expenses.append(expense if expense else 0)

        # Plot the bar chart
        plt.bar(categories, expenses)
        plt.xlabel('Categories')
        plt.ylabel('Expense Amount')
        plt.title('Expenses by Category')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        # Save the plot and display it in the Tkinter window
        plt.savefig("charts/expense_bar_chart.png")
        image = Image.open("charts/expense_bar_chart.png")
        image_resized = image.resize((500, 300))
        ctk_image = ctk.CTkImage(image_resized, size=(500, 300))
        image_label = ctk.CTkLabel(self.main_window_frame, image=ctk_image, text="")
        image_label.place(x=100, y=50)

    def show_expense_log(self):
        if hasattr(self, 'main_window_frame'):
            self.main_window_frame.destroy()

        self.landing_window.title("Expense Tracker | Expense Log")
        self.main_window_frame = ctk.CTkFrame(self.landing_window, height=550, width=700)
        self.main_window_frame.place(x=150, y=0)
         # From Date Selection
        from_date_label = ctk.CTkLabel(
            self.main_window_frame, text="From Date:", font=("Futura", 18))
        from_date_label.place(x=16, y=36)
        
        from_date_picker = tkcalendar.DateEntry(
            self.main_window_frame, width=16, font=("Helvetica", 14))
        from_date_picker.place(x=180, y=65)
        # To Date Selection
        to_date_label = ctk.CTkLabel(
            self.main_window_frame, text="To Date:", font=("Futura", 18))
        to_date_label.place(x=270, y=36)
        to_date_picker = tkcalendar.DateEntry(
            self.main_window_frame, width=16, font=("Helvetica", 14))
        to_date_picker.place(x=526, y=65)
        # Treeview to show expenses
        columns = ('Title', 'Date', 'Category', 'Amount')
        self.expense_tree = ttk.Treeview(
            self.main_window_frame, columns=columns, show='headings')
        
        for col in columns:
            self.expense_tree.heading(col, text=col)
            self.expense_tree.column(col, width=150)
        
        self.expense_tree.place(x=50, y=200, width=700, height=400)
                
        def fetch_expenses():
            # Clear previous entries
            for i in self.expense_tree.get_children():
                self.expense_tree.delete(i)
            
            from_date = from_date_picker.get_date().strftime("%Y-%m-%d")
            to_date = to_date_picker.get_date().strftime("%Y-%m-%d")
            cursor = self.connection.cursor()
            query = f"""
            SELECT expense_title_entry, date_added, expense_category, expense_amount 
            FROM expenses 
            WHERE date_added BETWEEN '{from_date}' AND '{to_date}'
            """
            cursor.execute(query)

            total_amount = 0
            for row in cursor.fetchall():
                self.expense_tree.insert('', 'end', values=row)
                total_amount += row[3]
            
            # Display the total expense amount
            total_label = ctk.CTkLabel( self.main_window_frame, text=f"Total Expenses: Rs. {total_amount:.3f}",
            font=("Futura", 16))
            total_label.place(x=50, y=500)
        
        fetch_button = ctk.CTkButton(
            self.main_window_frame, text="Fetch Expenses", 
            command=fetch_expenses, font=("Futura", 15))
        fetch_button.place(x=250, y=100)
    
    def currency_conversion_window(self):
        # Fix indentation error
        if hasattr(self, 'main_window_frame'):
            self.main_window_frame.destroy()

        self.landing_window.title("Expense Tracker | Currency Conversion")
        self.main_window_frame = ctk.CTkFrame(self.landing_window, height=550, width=750)
        self.main_window_frame.place(x=150, y=0)

        # Conversion label
        conversion_label = ctk.CTkLabel(self.main_window_frame, text="Currency Conversion", font=("Futura", 24, "bold"))
        conversion_label.place(x=250, y=40)

        # Entering the amount
        amount_label = ctk.CTkLabel(self.main_window_frame, text="Amount", font=("Futura", 18))
        amount_label.place(x=40, y=100)
        amount_entry = ctk.CTkEntry(self.main_window_frame, placeholder_text="Amount to Convert", width=160, corner_radius=5, height=10)
        amount_entry.place(x=200, y=100)

        # From currency dropdown
        from_currency_label = ctk.CTkLabel(self.main_window_frame, text="From Currency", font=("Futura", 18))
        from_currency_label.place(x=40, y=150)
        from_currency_dropdown = ctk.CTkComboBox(self.main_window_frame, width=160, values=["USD", "EUR", "INR", "GBP", "AUD","OMR"], state="readonly")
        from_currency_dropdown.set("USD")
        from_currency_dropdown.place(x=200, y=150)

        # To currency dropdown
        to_currency_label = ctk.CTkLabel(self.main_window_frame, text="To Currency", font=("Futura", 18))
        to_currency_label.place(x=40, y=200)
        to_currency_dropdown = ctk.CTkComboBox(self.main_window_frame, width=160, values=["USD", "EUR", "INR", "GBP", "AUD","OMR"], state="readonly")
        to_currency_dropdown.set("INR")
        to_currency_dropdown.place(x=200, y=200)

        # Result
        result_label = ctk.CTkLabel(self.main_window_frame, text="Converted Amount: -", font=("Futura", 18))
        result_label.place(x=200, y=300)

        def convert_currency():
            amount = amount_entry.get()
            from_currency = from_currency_dropdown.get()
            to_currency = to_currency_dropdown.get()

            if not amount or not amount.isdigit():
                messagebox.showerror("Invalid Input", "Please enter a valid amount.")
                return

            amount = float(amount)

            # Fetch the exchange rate from an API
            try:
                url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    exchange_rate = data["rates"].get(to_currency)

                    if exchange_rate:
                        converted_amount = amount * exchange_rate
                        result_label.configure(text=f"Converted Amount: {converted_amount:.2f} {to_currency}")
                    else:
                        messagebox.showerror("Error", "Currency conversion not available.")
                else:
                    messagebox.showerror("Error", "Failed to fetch exchange rate data.")

            except Exception as e:
                messagebox.showerror("Error", f"Error fetching exchange rate: {str(e)}")

        convert_button = ctk.CTkButton(self.main_window_frame, text="Convert", command=convert_currency, font=("Futura", 18))
        convert_button.place(x=200, y=250)

if __name__ == "__main__":
    app = ExpenseTracerApp()
    app.landing_window.mainloop()
