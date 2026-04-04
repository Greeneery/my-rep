from flask import Blueprint, render_template, request, redirect, url_for
from sql import execute_query


views = Blueprint('views', __name__, template_folder="template")

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/browse-page')
def browsePage():
    plants = []
    
    try:
        from sql import execute_query
        # Fetch plants from database
        query = "SELECT * FROM plants LIMIT 12"
        plants = execute_query(query, fetch="all")
    except Exception as e:
        print(f"Database error: {e}")
        plants = []
    
    # If no plants in database, use dummy data
    if not plants:
        plants = [
            {'id': i, 'name': 'Snake Plant', 'price': 25.00, 'image': 'homeBG.jpg'}
            for i in range(1, 7)
        ]
    
    return render_template("browsePage.html", plants=plants)

@views.route('/contact-page', methods=['GET', 'POST'])
def contactPage():
    if request.method == 'POST':
        user_name = request.form.get('name')
        user_email = request.form.get('email')
        user_message = request.form.get('user_message')
        query = "INSERT INTO Contact_Submissions(name, email, messageText) VALUES (%s, %s, %s)"
        params = (user_name, user_email, user_message)
        execute_query(query, params, fetch='none')
        return redirect(url_for('views.emailConfirmPage'))
    return render_template("contact.html")

@views.route('/check-out-page')
def checkout():
    return render_template("checkout.html")

@views.route('/detail-page')
def detail():
    return render_template("detail.html")

@views.route('/log-in-page')
def login():
    return render_template("logIn.html")

@views.route('/sign-up-page')
def signup():
    return render_template("signup.html")

@views.route('/favorites-page')
def favorites():
    return render_template("favorites.html")

@views.route('/cart-page')
def cart():
    return render_template("cart.html")

@views.route('/email-confirm-page')
def email_confirm():
    return render_template("emailConfirm.html")

@views.route('/purchase-confirm-page')
def purchase_confirm():
    return render_template("purchaseConfirm.html")
