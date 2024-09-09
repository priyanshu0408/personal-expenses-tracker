import csv
import os
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from datetime import datetime

# File to store expenses data
FILE_NAME = "expenses.csv"

# Create CSV if it doesn't exist
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Description", "Amount"])

# Add an expense
def add_expense(category, description, amount):
    with open(FILE_NAME, mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d"), category, description, amount])
    messagebox.showinfo("Success", "Expense added successfully!")

# View all expenses
def view_expenses():
    data = pd.read_csv(FILE_NAME)
    expenses_text.delete(1.0, tk.END)
    expenses_text.insert(tk.END, data.to_string(index=False))

# View total expenses and by category
def expense_summary():
    data = pd.read_csv(FILE_NAME)
    total_expenses = data['Amount'].sum()
    summary_text = f"Total Expenses: ${total_expenses:.2f}\n\n--- Expenses by Category ---\n"
    
    expenses_by_category = data.groupby("Category")["Amount"].sum()
    summary_text += expenses_by_category.to_string()

    summary_label.config(text=summary_text)

# Generate monthly report
def monthly_report():
    data = pd.read_csv(FILE_NAME)
    data['Date'] = pd.to_datetime(data['Date'])
    current_month = datetime.now().strftime("%Y-%m")
    monthly_data = data[data['Date'].dt.strftime("%Y-%m") == current_month]
    
    if monthly_data.empty:
        messagebox.showinfo("Monthly Report", "No expenses for this month.")
    else:
        expenses_text.delete(1.0, tk.END)
        expenses_text.insert(tk.END, monthly_data.to_string(index=False))

# Visualize expenses using a pie chart
def visualize_expenses():
    data = pd.read_csv(FILE_NAME)
    expenses_by_category = data.groupby("Category")["Amount"].sum()
    
    plt.pie(expenses_by_category, labels=expenses_by_category.index, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title("Expenses by Category")
    plt.show()

# GUI setup
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("600x600")

# Category Label and Entry
category_label = tk.Label(root, text="Category")
category_label.grid(row=0, column=0, padx=10, pady=10)
category_entry = ttk.Combobox(root, values=["Food", "Transport", "Bills", "Other"])
category_entry.grid(row=0, column=1, padx=10, pady=10)

# Description Label and Entry
description_label = tk.Label(root, text="Description")
description_label.grid(row=1, column=0, padx=10, pady=10)
description_entry = tk.Entry(root)
description_entry.grid(row=1, column=1, padx=10, pady=10)

# Amount Label and Entry
amount_label = tk.Label(root, text="Amount")
amount_label.grid(row=2, column=0, padx=10, pady=10)
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1, padx=10, pady=10)

# Add Expense Button
add_button = tk.Button(root, text="Add Expense", command=lambda: add_expense(category_entry.get(), description_entry.get(), float(amount_entry.get())))
add_button.grid(row=3, column=0, columnspan=2, pady=10)

# Expenses Text Box
expenses_text = tk.Text(root, height=15, width=50)
expenses_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# View All Expenses Button
view_button = tk.Button(root, text="View All Expenses", command=view_expenses)
view_button.grid(row=5, column=0, padx=10, pady=10)

# Generate Monthly Report Button
monthly_report_button = tk.Button(root, text="Generate Monthly Report", command=monthly_report)
monthly_report_button.grid(row=5, column=1, padx=10, pady=10)

# View Expense Summary Button
summary_label = tk.Label(root, text="")
summary_label.grid(row=6, column=0, columnspan=2)

summary_button = tk.Button(root, text="View Expense Summary", command=expense_summary)
summary_button.grid(row=7, column=0, columnspan=2, pady=10)

# Visualize Expenses Button
visualize_button = tk.Button(root, text="Visualize Expenses", command=visualize_expenses)
visualize_button.grid(row=8, column=0, columnspan=2, pady=10)

root.mainloop()
