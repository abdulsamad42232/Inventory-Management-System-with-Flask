---

# Inventory Management System using Flask

This is a simple web application built with Flask, a Python web framework, for managing inventory.

## Features

- Add items to the inventory with details such as item name, product ID, category, and quantity.
- View all items in the inventory.
- Delete items from the inventory.
- Increment or decrement the quantity of items.
- Search for items by product ID.

## Setup Instructions

1. Clone the repository to your local machine:
      
    ```bash
    git clone <repository-url>
    ```

2. Install dependencies by running this command in your code editor:
     
    ```bash
    pip install -r requirements.txt
    ```

3. Open the project folder and activate your virtual environment by running the following command in the terminal:
    
    ```bash
    activate myenv
    ```
     
4. Create a SQLite database and update the `SQLALCHEMY_DATABASE_URI` in `app.py` with your database URI by using the following commands in the terminal:

    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

5. Run the Flask app:

    ```bash
    python app.py
    ```

6. Open your web browser and navigate to `http://localhost:8000` to access the application.

## Usage

- To add an item to the inventory, fill out the form on the home page with the item details and click the "Submit" button.
- To delete an item, click the "Delete" button next to the item in the inventory.
- To increment or decrement the quantity of an item, click the "+" or "-" buttons, respectively.
- To search for an item by product ID, enter the product ID in the search bar and press Enter.

## Technologies Used

- Python
- Flask
- SQLAlchemy
- HTML
- Bootstrap

## Credits

- Developed by Abdul Samad Khan

## Contact

For any questions or feedback, please contact me at [abdulsamadkhan2001@gmail.com](mailto:abdulsamadkhan2001@gmail.com).

---
