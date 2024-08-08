from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import pytz
from sqlalchemy import event

# Initialize the Flask app
app = Flask(__name__)

# Configure the SQLAlchemy database URI
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:welcome2001@localhost/flask_tut_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy database object
db = SQLAlchemy(app)

# Initialize the Flask-Migrate object
migrate = Migrate(app, db)

# Define the Inventory model
class Inventory(db.Model):
    sno = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Product_ID = db.Column(db.String(100), nullable=False, unique=True)
    items = db.Column(db.String(200), nullable=False)
    Category = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    last_Updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.sno}-{self.items}'

# Define a listener to update the 'last_Updated' field on update
@event.listens_for(Inventory, 'before_update')
def receive_before_update(mapper, connection, target):
    target.last_Updated = datetime.utcnow()

# Function to convert UTC to local time (Pakistan Standard Time)
def convert_utc_to_local(utc_dt):
    local_tz = pytz.timezone('Asia/Karachi')  # Pakistan Standard Time zone
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)  # Normalize to handle daylight saving time changes

# Define the route for the index page
@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    searchResult = None

    # Handle POST request when adding new items to the inventory
    if request.method == 'POST':
        item = request.form['item']
        Product_ID = request.form['Product_ID']
        Category = request.form['Category']
        quantity = request.form['quantity']

        # Check if the Product ID already exists in the inventory
        if Inventory.query.filter_by(Product_ID=Product_ID).first():
            error = f'Product ID {Product_ID} already exists!'
        else:
            # Add the new item to the inventory
            inventory = Inventory(Product_ID=Product_ID, items=item, Category=Category, quantity=quantity)
            db.session.add(inventory)
            db.session.commit()

    # Handle search functionality
    if 'Product_ID' in request.args:
        searchProductID = request.args.get('Product_ID')
        searchResult = Inventory.query.filter_by(Product_ID=searchProductID).first()
        if searchResult:
            searchResult.last_Updated = convert_utc_to_local(searchResult.last_Updated)

    # Retrieve all items from the inventory and sort them by sno
    allInventory = Inventory.query.order_by(Inventory.sno).all()
    for item in allInventory:
        item.last_Updated = convert_utc_to_local(item.last_Updated)

    # Render the index.html template with inventory data, error message, and search result
    return render_template('index.html', allInventory=allInventory, error=error, searchResult=searchResult)

# Define the route to delete an item from the inventory
@app.route('/delete/<int:sno>')
def delete(sno):
    inventory = Inventory.query.filter_by(sno=sno).first()
    db.session.delete(inventory)
    db.session.commit()
    return redirect("/")

# Define the route to increment the quantity of an item
@app.route('/increment_quantity/<int:sno>', methods=['POST'])
def increment_quantity(sno):
    inventory = Inventory.query.get_or_404(sno)
    inventory.quantity += 1
    db.session.commit()
    return redirect("/")

# Define the route to decrement the quantity of an item
@app.route('/decrement_quantity/<int:sno>', methods=['POST'])
def decrement_quantity(sno):
    inventory = Inventory.query.get_or_404(sno)
    if inventory.quantity > 0:
        inventory.quantity -= 1
        db.session.commit()
    return redirect("/")

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=8000)
