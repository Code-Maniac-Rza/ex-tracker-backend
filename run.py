import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

class ExpenseTracker:
    def __init__(self):
        # Create static directory if it doesn't exist
        self.static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        os.makedirs(self.static_dir, exist_ok=True)
        
        # Set up data file path
        self.data_file = os.path.join(self.static_dir, 'expenses.json')
        self.expenses = []
        self.load_data()

    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as file:
                    self.expenses = json.load(file)
            else:
                self.expenses = []
                # Create initial empty file
                self.save_data()
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading data: {str(e)}")
            self.expenses = []

    def save_data(self):
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            with open(self.data_file, 'w') as file:
                json.dump(self.expenses, file, indent=4)
        except IOError as e:
            print(f"Error saving data: {str(e)}")

    def add_expense(self, args):
        if len(args) < 3:
            return "Invalid input. Format: add <amount> <category> <description>\n"
            
        try:
            amount = float(args[0])
            category = args[1]
            description = " ".join(args[2:])
            date = datetime.today().strftime('%Y-%m-%d')

            expense = {
                "amount": amount,
                "category": category,
                "date": date,
                "description": description
            }
            self.expenses.append(expense)
            self.save_data()
            return f"Expense added successfully: {amount} {category} - {description}\n"
        except ValueError:
            return "Invalid amount. Please enter a valid number.\n"
        except Exception as e:
            return f"Error adding expense: {str(e)}\n"

    def view_expenses(self, args):
        try:
            category_filter = args[0] if args else None
            filtered_expenses = [
                e for e in self.expenses if not category_filter or e['category'] == category_filter
            ]

            if not filtered_expenses:
                return "No expenses to show.\n"

            response = "Current expenses:\n"
            for i, expense in enumerate(filtered_expenses, start=1):
                response += (
                    f"{i}. {expense['date']} - {expense['category']}: ${expense['amount']:.2f} "
                    f"({expense['description']})\n"
                )
            return response
        except Exception as e:
            return f"Error viewing expenses: {str(e)}\n"

    def delete_expense(self, args):
        try:
            if not args:
                return "Error: Please provide an index to delete. Format: delete <index>\n"
                
            index = int(args[0]) - 1
            if 0 <= index < len(self.expenses):
                removed = self.expenses.pop(index)
                self.save_data()
                return f"Deleted: {removed['description']} (${removed['amount']:.2f} {removed['category']}).\n"
            else:
                return "Invalid index. Please provide a valid expense number.\n"
        except ValueError:
            return "Error: Please provide a valid number for the index.\n"
        except Exception as e:
            return f"Error deleting expense: {str(e)}\n"

    def generate_report(self):
        try:
            if not self.expenses:
                return "No expenses to report.\n"

            categories = {}
            for expense in self.expenses:
                categories[expense['category']] = categories.get(expense['category'], 0) + expense['amount']

            # Generate the bar chart
            plt.figure(figsize=(10, 6))
            plt.bar(categories.keys(), categories.values(), color="skyblue")
            plt.title("Expense Distribution by Category")
            plt.xlabel("Category")
            plt.ylabel("Amount Spent ($)")
            plt.xticks(rotation=45)
            
            # Format y-axis with currency
            plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.2f}'))

            # Adjust layout to prevent label cutoff
            plt.tight_layout()

            # Save the plot as an image
            report_path = os.path.join(self.static_dir, "report.png")
            plt.savefig(report_path)
            plt.close()

            return f"Report generated successfully. Check 'static/report.png'.\n"
        except Exception as e:
            return f"Error generating report: {str(e)}\n"

    def run(self):
        print("Welcome to Expense Tracker! Available commands:")
        print("  add <amount> <category> <description>")
        print("  view [category]")
        print("  delete <index>")
        print("  generate")
        print("  exit")
        
        while True:
            try:
                command = input().strip()
                if command.startswith("add "):
                    response = self.add_expense(command.split()[1:])
                elif command.startswith("view"):
                    args = command.split()[1:]  # Optional category filter
                    response = self.view_expenses(args)
                elif command.startswith("delete "):
                    response = self.delete_expense(command.split()[1:])
                elif command == "generate":
                    response = self.generate_report()
                elif command == "exit":
                    print("Goodbye!")
                    break
                else:
                    response = "Invalid command. Use 'add', 'view', 'delete', 'generate', or 'exit'.\n"
                print(response, end="")
            except EOFError:
                break
            except Exception as e:
                print(f"Unexpected error: {str(e)}\n")

if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()