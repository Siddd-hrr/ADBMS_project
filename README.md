# Expense Tracker

A desktop-based Expense Tracker application developed using **Python, CustomTkinter, and MongoDB Atlas**. The application allows users to record, view, update, delete, search, and filter their daily expenses through a graphical user interface.

The project is designed to provide a simple way to manage personal expenses, categorize spending, track payment methods, and calculate total expenditure.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [MongoDB Atlas Configuration](#mongodb-atlas-configuration)
- [Running the Application Locally](#running-the-application-locally)
- [How to Use](#how-to-use)
- [Input Validation](#input-validation)
- [Database Structure](#database-structure)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)

## Project Overview

The Expense Tracker is a Python desktop application that uses a graphical user interface to manage expense records. It connects directly to MongoDB Atlas to store and retrieve data, without requiring a separate backend server or REST API.

Each expense record contains information such as the expense title, amount, category, date, payment method, and an optional description.

The application follows a modular structure that separates database connectivity, data models, validation, expense operations, and the graphical interface.

## Features

- **Create Expenses:** Add new expense records with relevant details.
- **View Expenses:** Display saved expenses in a table.
- **Update Expenses:** Select an existing expense and modify its information.
- **Delete Expenses:** Remove expenses after confirming the deletion.
- **Search Expenses:** Search expense titles and descriptions.
- **Filter Expenses:** Filter records by category and payment method.
- **Expense Summary:** Display the total expenditure and number of matching records.
- **Input Validation:** Validate amounts, titles, dates, categories, payment methods, and descriptions.
- **Future-Date Restriction:** Prevent users from recording expenses with future dates.
- **Cloud Database:** Store expense records in MongoDB Atlas.
- **Error Handling:** Display messages when validation or database operations fail.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.12 | Core application programming language |
| CustomTkinter | Modern desktop graphical user interface |
| Tkinter / ttk | Table, dialogs, and supporting GUI components |
| MongoDB Atlas | Cloud-hosted NoSQL database |
| PyMongo | Python driver for MongoDB |
| python-dotenv | Load database credentials from a `.env` file |
| uv | Python dependency and environment management |
| VS Code | Development environment |
| Git | Optional source-code version control |

## Requirements

Before running the project, install or configure the following:

1. **Python 3.12 or compatible Python version**  
   Download: https://www.python.org/downloads/

2. **uv package manager**  
   Installation instructions: https://docs.astral.sh/uv/getting-started/installation/

3. **Visual Studio Code**  
   Download: https://code.visualstudio.com/

4. **MongoDB Atlas account**  
   Create a free cluster if you do not already have one: https://www.mongodb.com/atlas

5. **Internet connection**  
   Required to access the MongoDB Atlas cluster.

6. **Git (optional)**  
   Useful for version control and collaboration.

No separate Node.js installation, web server, or backend API is required.

## Project Structure

```text
expense-tracker/
│
├── .env
├── .env.example
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
├── README.md
│
└── src/
    └── expense_tracker/
        ├── __init__.py
        ├── main.py
        ├── gui.py
        ├── database.py
        ├── models.py
        ├── validators.py
        └── expense_service.py
```

### Description of Important Files

- `main.py`: Entry point used to launch the desktop application.
- `gui.py`: Implements the graphical interface, forms, expense table, filters, and buttons.
- `database.py`: Manages the MongoDB Atlas connection.
- `models.py`: Defines the expense data model and converts data to and from MongoDB-compatible types.
- `validators.py`: Contains input validation functions.
- `expense_service.py`: Implements expense CRUD operations, searching, filtering, and summary calculations.
- `pyproject.toml`: Defines project metadata, dependencies, and the application command.
- `uv.lock`: Records resolved dependency versions for reproducible installations.
- `.env`: Stores the MongoDB connection URI locally.
- `.env.example`: Provides a template for the required environment variable.
- `.gitignore`: Excludes virtual environments, local credentials, and generated files from Git.

## Installation and Setup

### Step 1: Clone the Repository (Optional)

If the project is hosted in a Git repository, clone it using:

```bash
git clone <your-repository-url>
cd expense-tracker
```

Alternatively, open your existing project folder directly in VS Code.

### Step 2: Open the Project in VS Code

Open the project directory and select **Terminal → New Terminal**.

Make sure the terminal is in the root directory containing `pyproject.toml`.

### Step 3: Install Dependencies

Run:

```bash
uv sync
```

This command creates or updates the project's virtual environment and installs the dependencies declared in `pyproject.toml`.

The project uses the following main Python packages:

- `customtkinter`
- `pymongo`
- `python-dotenv`

If Python 3.12 is installed and the project requires it, configure the interpreter using:

```bash
uv python pin 3.12
```

Then run `uv sync` again if necessary.

## MongoDB Atlas Configuration

The application uses MongoDB Atlas as its database.

### Step 1: Create a Database User

1. Sign in to MongoDB Atlas.
2. Open your cluster.
3. Navigate to **Database Access**.
4. Create a database user with an appropriate username and password.

Use credentials dedicated to this application rather than sharing an administrator account.

### Step 2: Configure Network Access

1. Open **Network Access** in Atlas.
2. Add your current public IP address.
3. Save the configuration.

Avoid allowing access from every IP address unless you understand the security implications.

### Step 3: Obtain the Connection URI

1. Open your Atlas cluster.
2. Select **Connect**.
3. Choose the Python driver connection option.
4. Copy the provided connection URI.
5. Replace the username, password, and other placeholders as required.

### Step 4: Create the `.env` File

Create a file named `.env` in the project root, next to `pyproject.toml`.

Add:

```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-host>/
```

Replace the example value with your actual Atlas connection URI.

If your password contains special characters, ensure they are URL-encoded in the URI.

**Security note:** Never commit `.env` to Git or publish your database credentials. The `.gitignore` file should include `.env`.

The application uses the following database and collection names:

```text
Database:   expense_tracker
Collection: expenses
```

The collection can be created automatically by MongoDB when the application first inserts an expense.

## Running the Application Locally

After installing the dependencies and configuring MongoDB Atlas, run the following command from the project root:

```bash
uv run expense-tracker
```

If the console-script entry point is unavailable, use:

```bash
uv run python -m expense_tracker.main
```

The Expense Tracker desktop window should open.

### Local Hosting Explanation

This is a **desktop application**, not a website. Running it locally launches the graphical interface on your computer; it does not start an HTTP server or provide a browser URL such as `http://localhost:8000`.

The application connects to MongoDB Atlas over the internet to store and retrieve expense data.

## How to Use

### Add an Expense

1. Enter the expense title.
2. Enter the amount in Indian Rupees (₹).
3. Select a category.
4. Enter the expense date in `YYYY-MM-DD` format.
5. Select the payment method.
6. Optionally enter a description.
7. Click **Add Expense**.

### View Expenses

Saved expenses appear in the table on the main screen.

The table displays the title, amount, category, date, and payment method.

### Update an Expense

1. Select a row in the table.
2. Edit the information in the expense form.
3. Click **Update Selected**.

### Delete an Expense

1. Select the expense to remove.
2. Click **Delete Selected**.
3. Confirm the deletion in the confirmation dialog.

### Search and Filter

- Enter a keyword to search expense titles or descriptions.
- Select a category to filter by expense category.
- Select a payment method to filter by payment type.
- Click **Search / Filter** to refresh the displayed results.

The total expenditure and record count reflect the currently displayed matching records.

## Input Validation

The application validates user input before performing database operations.

| Field | Validation |
|---|---|
| Title | Required; 2–80 characters |
| Amount | Must be positive and have no more than two decimal places |
| Category | Must match one of the supported categories |
| Date | Must be valid and cannot be in the future |
| Payment method | Must match one of the supported methods |
| Description | Optional; maximum 250 characters |

### Supported Expense Categories

- Food & Dining
- Transport
- Education
- Shopping
- Bills
- Healthcare
- Other

### Supported Payment Methods

- Cash
- UPI
- Card
- Bank Transfer

## Database Structure

Each expense is stored as a document in the `expenses` collection.

Example document:

```json
{
  "_id": "MongoDB ObjectId",
  "title": "Lunch",
  "amount": "150.50",
  "category": "Food & Dining",
  "date": "2026-10-18T00:00:00Z",
  "payment_method": "UPI",
  "description": "Lunch at college",
  "created_at": "UTC timestamp",
  "updated_at": "UTC timestamp"
}
```

The example is illustrative. In the actual database, `_id` is an ObjectId, `amount` is stored as BSON Decimal128, and the date and timestamps use MongoDB date types.

### Database Operations

The project implements the following CRUD operations:

- **Create:** Insert a new expense using `insert_one()`.
- **Read:** Retrieve matching expenses using `find()`.
- **Update:** Modify an existing expense using `update_one()`.
- **Delete:** Remove an expense using `delete_one()`.

Each expense is identified by its MongoDB `_id`, rather than its title, so records with identical titles can still be managed independently.

## Troubleshooting

### 1. MongoDB Connection Failed

Check the following:

- The `.env` file is in the project root.
- The variable name is exactly `MONGODB_URI`.
- The Atlas URI and credentials are correct.
- Your current IP address is allowed in Atlas Network Access.
- Your cluster is running and your internet connection is available.

### 2. `uv` Command Not Found

Install `uv` using the official installation instructions and restart your terminal.

Documentation: https://docs.astral.sh/uv/

### 3. Module Not Found

Run the following from the project root:

```bash
uv sync
```

Then launch the application through `uv run`.

### 4. Application Does Not Open

Run the application from the VS Code terminal:

```bash
uv run python -m expense_tracker.main
```

Read the error message printed in the terminal. Check that the required files are present and that the entry point imports the GUI correctly.

### 5. Atlas Authentication Error

Verify the database username and password. If the password contains reserved URL characters, encode them correctly in the connection URI.

## Future Improvements

Possible future enhancements include:

- Monthly and yearly expense reports.
- Category-wise spending charts.
- Date-range filtering.
- Exporting expenses to CSV or Excel.
- Budget limits and budget alerts.
- A dashboard with spending trends.
- Automated tests for validation and CRUD operations.
- Optional offline data entry and synchronization.

## License

This project was developed for educational and personal expense-management purposes. Add a license file if you plan to distribute the source code publicly.
