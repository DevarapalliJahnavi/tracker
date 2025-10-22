# Expense Tracker

A simple and intuitive web application for tracking your daily expenses. Built with Flask and SQLite, this application provides a clean user interface to manage, categorize, and visualize your spending.

## Features

- **Add, Edit, and Delete Expenses:** Easily manage your expense records.
- **Expense Categorization:** Assign categories to your expenses for better organization.
- **Interactive Dashboard:** Visualize your spending patterns with interactive charts.
- **Responsive Design:** Access and manage your expenses on any device.
- **Theme Customization:** Switch between light and dark themes.

## Project Structure

The project is organized as follows:

```
/
├── app.py              # Main Flask application file
├── db_utils.py         # Database utility functions
├── expense.db          # SQLite database file
├── requirements.txt    # Python dependencies
├── routes/             # Flask blueprints for different routes
│   ├── api.py          # API endpoints
│   ├── dashboard.py    # Dashboard and home page
│   └── expense.py      # Expense management routes
├── static/             # Static assets (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── img/
└── templates/          # HTML templates
    ├── index.html
    ├── add_expense.html
    ├── edit_expense.html
    └── stats.html
```

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/expense-tracker.git
    cd expense-tracker
    ```

2.  **Create a virtual environment and activate it:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Flask application:**

    ```bash
    python app.py
    ```

2.  **Open your web browser and navigate to:**

    ```
    http://127.0.0.1:5000
    ```

## Dependencies

The project relies on the following Python libraries:

-   [Flask](https://flask.palletsprojects.com/)
-   [Jinja2](https://jinja.palletsprojects.com/)
-   [itsdangerous](https://itsdangerous.palletsprojects.com/)
-   [Werkzeug](https://werkzeug.palletsprojects.com/)
-   [click](https://click.palletsprojects.com/)

Frontend libraries (loaded via CDN):

-   [Bootstrap](https://getbootstrap.com/)
-   [Chart.js](https://www.chartjs.org/)
-   [AOS (Animate On Scroll)](https://michalsnik.github.io/aos/)
-   [Rellax.js](https://dixonandmoe.com/rellax/)
-   [CountUp.js](https://inorganik.github.io/countUp.js/)

## API Endpoints

The application exposes the following API endpoints:

-   `GET /api/expenses`: Retrieve all expenses.
-   `GET /api/budget`: Retrieve the current budget.
-   `POST /update_budget`: Update the budget.

*(Note: This is a simplified list. Refer to `routes/api.py` for more details.)*

## Error Handling

The application includes custom error pages for `404 Not Found` and `500 Internal Server Error`.

## Contributing

Contributions are welcome! If you have any suggestions or find any bugs, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
