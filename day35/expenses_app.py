import csv
import os
from dataclasses import dataclass
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(APP_DIR, "expenses.csv")
CATEGORIES = ["Food", "Transport", "Utilities", "Entertainment", "Health", "Shopping", "Other"]


@dataclass
class Expense:
    date: str
    category: str
    amount: float
    description: str

    def to_row(self) -> list[str]:
        return [self.date, self.category, f"{self.amount:.2f}", self.description]

    @staticmethod
    def from_row(row: list[str]) -> "Expense":
        date, category, amount, description = row
        return Expense(date=date, category=category, amount=float(amount), description=description)


class ExpenseApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("760x520")
        self.root.minsize(700, 480)

        self.expenses: list[Expense] = []

        self.category_var = tk.StringVar(value=CATEGORIES[0])
        self.amount_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        self.total_var = tk.StringVar(value="Total: $0.00")

        self._build_ui()
        self._load_expenses()
        self._refresh_listbox()

    def _build_ui(self) -> None:
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill=tk.BOTH, expand=True)

        input_frame = ttk.LabelFrame(main, text="Add Expense", padding=12)
        input_frame.pack(fill=tk.X)

        ttk.Label(input_frame, text="Category").grid(row=0, column=0, sticky=tk.W, padx=4, pady=4)
        category_menu = ttk.OptionMenu(input_frame, self.category_var, self.category_var.get(), *CATEGORIES)
        category_menu.grid(row=0, column=1, sticky=tk.W, padx=4, pady=4)

        ttk.Label(input_frame, text="Amount").grid(row=0, column=2, sticky=tk.W, padx=4, pady=4)
        amount_entry = ttk.Entry(input_frame, textvariable=self.amount_var, width=12)
        amount_entry.grid(row=0, column=3, sticky=tk.W, padx=4, pady=4)

        ttk.Label(input_frame, text="Description").grid(row=0, column=4, sticky=tk.W, padx=4, pady=4)
        desc_entry = ttk.Entry(input_frame, textvariable=self.desc_var, width=30)
        desc_entry.grid(row=0, column=5, sticky=tk.W, padx=4, pady=4)

        add_btn = ttk.Button(input_frame, text="Add", command=self.add_expense)
        add_btn.grid(row=0, column=6, sticky=tk.W, padx=6, pady=4)

        input_frame.columnconfigure(5, weight=1)

        list_frame = ttk.LabelFrame(main, text="Expense History", padding=12)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=12)

        self.listbox = tk.Listbox(list_frame, height=14)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        bottom = ttk.Frame(main)
        bottom.pack(fill=tk.X)

        total_label = ttk.Label(bottom, textvariable=self.total_var, font=("Segoe UI", 11, "bold"))
        total_label.pack(side=tk.LEFT, padx=4)

        buttons = ttk.Frame(bottom)
        buttons.pack(side=tk.RIGHT)

        ttk.Button(buttons, text="Delete Selected", command=self.delete_selected).pack(side=tk.LEFT, padx=4)
        ttk.Button(buttons, text="Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=4)
        ttk.Button(buttons, text="Save", command=self.save_expenses).pack(side=tk.LEFT, padx=4)
        ttk.Button(buttons, text="Export CSV", command=self.export_csv).pack(side=tk.LEFT, padx=4)

        self.root.bind("<Return>", lambda _event: self.add_expense())

    def add_expense(self) -> None:
        amount_text = self.amount_var.get().strip()
        desc = self.desc_var.get().strip()
        category = self.category_var.get().strip()

        if not amount_text:
            messagebox.showwarning("Missing Amount", "Please enter an amount.")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror("Invalid Amount", "Amount must be a number.")
            return

        if amount <= 0:
            messagebox.showerror("Invalid Amount", "Amount must be greater than zero.")
            return

        if not desc:
            desc = "-"

        date = datetime.now().strftime("%Y-%m-%d")
        expense = Expense(date=date, category=category, amount=amount, description=desc)
        self.expenses.append(expense)

        self.amount_var.set("")
        self.desc_var.set("")
        self._refresh_listbox()
        self.save_expenses()

    def delete_selected(self) -> None:
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("No Selection", "Select an expense to delete.")
            return

        for index in reversed(selection):
            del self.expenses[index]

        self._refresh_listbox()
        self.save_expenses()

    def clear_all(self) -> None:
        if not self.expenses:
            return
        if not messagebox.askyesno("Clear All", "Delete all expenses?"):
            return
        self.expenses.clear()
        self._refresh_listbox()
        self.save_expenses()

    def _refresh_listbox(self) -> None:
        self.listbox.delete(0, tk.END)
        total = 0.0
        for expense in self.expenses:
            total += expense.amount
            line = f"{expense.date} | {expense.category:<13} | ${expense.amount:>8.2f} | {expense.description}"
            self.listbox.insert(tk.END, line)
        self.total_var.set(f"Total: ${total:.2f}")

    def _load_expenses(self) -> None:
        if not os.path.exists(DATA_FILE):
            return
        try:
            with open(DATA_FILE, newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) != 4:
                        continue
                    try:
                        self.expenses.append(Expense.from_row(row))
                    except ValueError:
                        continue
        except OSError:
            messagebox.showwarning("Load Error", "Could not load saved expenses.")

    def save_expenses(self) -> None:
        try:
            with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Category", "Amount", "Description"])
                for expense in self.expenses:
                    writer.writerow(expense.to_row())
        except OSError:
            messagebox.showerror("Save Error", "Could not save expenses.")

    def export_csv(self) -> None:
        if not self.expenses:
            messagebox.showinfo("No Data", "No expenses to export.")
            return
        file_path = filedialog.asksaveasfilename(
            title="Export Expenses",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
        )
        if not file_path:
            return
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Category", "Amount", "Description"])
                for expense in self.expenses:
                    writer.writerow(expense.to_row())
        except OSError:
            messagebox.showerror("Export Error", "Could not export expenses.")


def main() -> None:
    root = tk.Tk()
    style = ttk.Style()
    if "clam" in style.theme_names():
        style.theme_use("clam")
    ExpenseApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
