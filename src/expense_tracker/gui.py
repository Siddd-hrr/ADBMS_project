
"""CustomTkinter desktop interface for Expense Tracker."""

import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal
from datetime import date
from bson import ObjectId
import customtkinter as ctk

from .database import close_connection
from .expense_service import ExpenseService
from .models import Expense
from .validators import (
    CATEGORIES,
    PAYMENT_METHODS,
    ValidationError,
    validate_title,
    parse_amount,
    validate_category,
    validate_payment_method,
    parse_expense_date,
    validate_description,
)


class ExpenseTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Expense Tracker")
        self.geometry("1180x720")
        self.minsize(1000, 650)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.service = ExpenseService()
        self.selected_id = None
        self.expenses_by_id = {}

        self.search_var = tk.StringVar()
        self.category_filter = tk.StringVar(value="All")
        self.payment_filter = tk.StringVar(value="All")

        self._build_layout()
        self._build_table_style()
        self.refresh_expenses()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left: expense form
        self.form_frame = ctk.CTkFrame(self, width=320)
        self.form_frame.grid(
            row=0, column=0, sticky="nsw", padx=12, pady=12
        )
        self.form_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.form_frame,
            text="Expense Details",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).grid(row=0, column=0, padx=16, pady=(18, 14))

        self.title_entry = self._entry("Title", 1)
        self.amount_entry = self._entry("Amount (₹)", 3)

        ctk.CTkLabel(
            self.form_frame, text="Category"
        ).grid(row=5, column=0, sticky="w", padx=16, pady=(8, 2))

        self.category_box = ctk.CTkComboBox(
            self.form_frame,
            values=CATEGORIES,
            state="readonly",
        )
        self.category_box.set(CATEGORIES[0])
        self.category_box.grid(
            row=6, column=0, sticky="ew", padx=16, pady=(0, 6)
        )

        ctk.CTkLabel(
            self.form_frame, text="Date (YYYY-MM-DD)"
        ).grid(row=7, column=0, sticky="w", padx=16, pady=(8, 2))

        self.date_entry = ctk.CTkEntry(
            self.form_frame, placeholder_text="2026-10-17"
        )
        self.date_entry.insert(0, date.today().isoformat())
        self.date_entry.grid(
            row=8, column=0, sticky="ew", padx=16, pady=(0, 6)
        )

        ctk.CTkLabel(
            self.form_frame, text="Payment Method"
        ).grid(row=9, column=0, sticky="w", padx=16, pady=(8, 2))

        self.payment_box = ctk.CTkComboBox(
            self.form_frame,
            values=PAYMENT_METHODS,
            state="readonly",
        )
        self.payment_box.set(PAYMENT_METHODS[0])
        self.payment_box.grid(
            row=10, column=0, sticky="ew", padx=16, pady=(0, 6)
        )

        ctk.CTkLabel(
            self.form_frame, text="Description (optional)"
        ).grid(row=11, column=0, sticky="w", padx=16, pady=(8, 2))

        self.description_box = ctk.CTkTextbox(
            self.form_frame, height=70
        )
        self.description_box.grid(
            row=12, column=0, sticky="ew", padx=16, pady=(0, 10)
        )

        self.save_button = ctk.CTkButton(
            self.form_frame,
            text="Add Expense",
            command=self.save_expense,
        )
        self.save_button.grid(
            row=13, column=0, sticky="ew", padx=16, pady=5
        )

        ctk.CTkButton(
            self.form_frame,
            text="Clear Form",
            command=self.clear_form,
            fg_color="gray",
            hover_color="dim gray",
        ).grid(row=14, column=0, sticky="ew", padx=16, pady=5)

        # Right: table and filters
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(
            row=0, column=1, sticky="nsew", padx=(0, 12), pady=12
        )
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self.content_frame,
            text="My Expenses",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(16, 10))

        filters = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        filters.grid(row=1, column=0, sticky="ew", padx=12, pady=4)
        filters.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            filters,
            textvariable=self.search_var,
            placeholder_text="Search title or description...",
        )
        self.search_entry.grid(
            row=0, column=0, sticky="ew", padx=4, pady=4
        )

        self.filter_category_box = ctk.CTkComboBox(
            filters,
            values=["All"] + CATEGORIES,
            variable=self.category_filter,
            state="readonly",
            width=145,
        )
        self.filter_category_box.grid(row=0, column=1, padx=4, pady=4)

        self.filter_payment_box = ctk.CTkComboBox(
            filters,
            values=["All"] + PAYMENT_METHODS,
            variable=self.payment_filter,
            state="readonly",
            width=140,
        )
        self.filter_payment_box.grid(row=0, column=2, padx=4, pady=4)

        ctk.CTkButton(
            filters,
            text="Search / Filter",
            width=110,
            command=self.refresh_expenses,
        ).grid(row=0, column=3, padx=4, pady=4)

        table_frame = ctk.CTkFrame(
            self.content_frame, fg_color="transparent"
        )
        table_frame.grid(
            row=2, column=0, sticky="nsew", padx=12, pady=8
        )
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        columns = (
            "title", "amount", "category", "date", "payment"
        )
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        headings = {
            "title": "Title",
            "amount": "Amount (₹)",
            "category": "Category",
            "date": "Date",
            "payment": "Payment",
        }

        widths = {
            "title": 180,
            "amount": 100,
            "category": 130,
            "date": 105,
            "payment": 115,
        }

        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(
                column, width=widths[column], anchor="w"
            )

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        actions = ctk.CTkFrame(
            self.content_frame, fg_color="transparent"
        )
        actions.grid(row=3, column=0, sticky="ew", padx=12, pady=4)

        ctk.CTkButton(
            actions,
            text="Update Selected",
            command=self.update_selected,
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            actions,
            text="Delete Selected",
            command=self.delete_selected,
            fg_color="#B33A3A",
            hover_color="#8F2D2D",
        ).pack(side="left", padx=4)

        self.summary_label = ctk.CTkLabel(
            self.content_frame,
            text="Total: ₹0.00 | Records: 0",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.summary_label.grid(
            row=4, column=0, sticky="w", padx=16, pady=(8, 16)
        )

    def _entry(self, label, row):
        ctk.CTkLabel(
            self.form_frame, text=label
        ).grid(row=row, column=0, sticky="w", padx=16, pady=(8, 2))

        entry = ctk.CTkEntry(self.form_frame)
        entry.grid(
            row=row + 1, column=0, sticky="ew", padx=16, pady=(0, 6)
        )
        return entry

    def _build_table_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            rowheight=30,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
        )

    def _read_form(self):
        title = validate_title(self.title_entry.get())
        amount = parse_amount(self.amount_entry.get())
        category = validate_category(self.category_box.get())
        expense_date = parse_expense_date(self.date_entry.get())
        payment = validate_payment_method(self.payment_box.get())
        description = validate_description(
            self.description_box.get("1.0", "end").strip()
        )

        return Expense(
            title=title,
            amount=amount,
            category=category,
            date=expense_date,
            payment_method=payment,
            description=description,
        )

    def save_expense(self):
        try:
            expense = self._read_form()
            self.service.create(expense)
        except ValidationError as exc:
            messagebox.showwarning("Invalid Input", str(exc))
            return
        except Exception as exc:
            messagebox.showerror(
                "Save Failed",
                f"Could not save the expense.\n\n{exc}",
            )
            return

        messagebox.showinfo("Success", "Expense added successfully.")
        self.clear_form()
        self.refresh_expenses()

    def update_selected(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "Select Expense", "Select an expense from the table first."
            )
            return

        try:
            expense = self._read_form()
            self.service.update(self.selected_id, expense)
        except ValidationError as exc:
            messagebox.showwarning("Invalid Input", str(exc))
            return
        except Exception as exc:
            messagebox.showerror(
                "Update Failed",
                f"Could not update the expense.\n\n{exc}",
            )
            return

        messagebox.showinfo("Success", "Expense updated successfully.")
        self.clear_form()
        self.refresh_expenses()

    def delete_selected(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "Select Expense", "Select an expense from the table first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete the selected expense?",
        )
        if not confirm:
            return

        try:
            self.service.delete(self.selected_id)
        except Exception as exc:
            messagebox.showerror(
                "Delete Failed",
                f"Could not delete the expense.\n\n{exc}",
            )
            return

        self.clear_form()
        self.refresh_expenses()
        messagebox.showinfo("Success", "Expense deleted successfully.")

    def refresh_expenses(self):
        try:
            expenses = self.service.list_expenses(
                search=self.search_var.get(),
                category=self.category_filter.get(),
                payment_method=self.payment_filter.get(),
            )
        except Exception as exc:
            messagebox.showerror(
                "Database Error",
                "Could not load expenses.\n\n"
                f"{exc}\n\n"
                "Check your .env file and MongoDB Atlas access settings.",
            )
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.expenses_by_id.clear()

        total = Decimal("0.00")

        for expense in expenses:
            expense_id = str(expense.id)
            self.expenses_by_id[expense_id] = expense
            total += expense.amount

            self.tree.insert(
                "",
                "end",
                iid=expense_id,
                values=(
                    expense.title,
                    f"{expense.amount:,.2f}",
                    expense.category,
                    expense.date.isoformat(),
                    expense.payment_method,
                ),
            )

        self.summary_label.configure(
            text=f"Total: ₹{total:,.2f} | Records: {len(expenses)}"
        )

    def on_select(self, _event=None):
        selected = self.tree.selection()
        if not selected:
            return

        expense_id = selected[0]
        expense = self.expenses_by_id.get(expense_id)
        if expense is None:
            return

        self.selected_id = ObjectId(expense_id)

        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, expense.title)

        self.amount_entry.delete(0, "end")
        self.amount_entry.insert(0, str(expense.amount))

        self.category_box.set(expense.category)
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, expense.date.isoformat())
        self.payment_box.set(expense.payment_method)

        self.description_box.delete("1.0", "end")
        self.description_box.insert("1.0", expense.description)

        self.save_button.configure(text="Add Expense")

    def clear_form(self):
        self.selected_id = None

        self.title_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")

        self.category_box.set(CATEGORIES[0])
        self.payment_box.set(PAYMENT_METHODS[0])

        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, date.today().isoformat())

        self.description_box.delete("1.0", "end")

        for item in self.tree.selection():
            self.tree.selection_remove(item)

        self.save_button.configure(text="Add Expense")

    def on_close(self):
        try:
            close_connection()
        finally:
            self.destroy()
