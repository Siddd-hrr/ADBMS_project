
"""Start the Expense Tracker desktop application."""

from .gui import ExpenseTrackerApp


def main():
    app = ExpenseTrackerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
