from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, SignupForm
import models
import auth
from sql import execute_query
from auth import login_required


views = Blueprint('views', __name__, template_folder="template")

@views.route('/')
@login_required
def home():
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    return render_template("home.html", user = user_data)

@views.route('/browse-page')
def browse():
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    return render_template("browse.html", user = user_data)

@views.route('/contact-page')
def contact():
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    return render_template("contact.html", user = user_data)

@views.route('/check-out-page')
def checkout():
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    
    return render_template("checkout.html")

@views.route('/detail-page')
def detail():
    return render_template("detail.html")

@views.route('/log-in-page', methods=["GET", "POST"])
def login():
    form = LoginForm()
    message = ""
    
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                result, status_code = auth.authenticate_user(
                    form.name.data, form.password.data
                )
                if status_code == 200:
                    print("SUCCESS!")
                    token = auth.generate_token(
                        result["user_id"], result["username"]
                    )
                    response = redirect(url_for("views.home"))
                    response.set_cookie(
                        "auth_token",
                        token,
                        max_age=86400,
                        httponly=True,
                        secure=False,
                        samesite="Lax",
                    )
                    return response
                else:
                    message = result.get("error", "Login failed")
            except Exception as e:
                message = f"Login failed: {str(e)}"
    return render_template("logIn.html", form=form, message=message)

@views.route('/sign-up-page', methods=['GET','POST'])
def signup():
    form = SignupForm()
    message = ""
    
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                result, status_code = auth.create_user_account(
                    form.username.data,
                    form.password.data,
                    form.password2.data,
                    form.first_name.data,
                    form.last_name.data,
                    form.email.data,
                )
                
                if status_code == 201:
                    return redirect(
                        url_for("views.login",
                             message="Account created successfully! Yay! Pls Login. Nyan~",   
                        )
                    )
                else:
                    message = result.get("error", "Signup failed")
            except Exception as e:
                message = f"Signup failed: {str(e)}"
                       
    return render_template("signup.html", form=form, message=message)

@views.route('/logout')
def logout():
    response = redirect(url_for("views.index"))
    response.set_cookie("auth_token", "", expires=0)
    return response

@views.route('/favorites-page')
def favorites():
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    return render_template("favorites.html", user = user_data)

@views.route('/cart-page')
def cart():
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    return render_template("cart.html", user = user_data)

@views.route('/add-to-cart/<int:plant_id>', methods=['POST'])
def add_to_cart(plant_id):
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    
    if user_data is None:
        return redirect(url_for('views.login'))
    
    user_id = user_data['user_id']
    cart_id = models.get_or_create_cart(user_id)
    
    check_query = "SELECT cartItemID, quantity FROM Cart_Items WHERE cartID = %s AND plantID = %s"
    existing_item = execute_query(check_query, (cart_id, plant_id), fetch="one")
    
    if existing_item:
        new_quty = existing_item['quantity'] + 1
        update_query = "UPDATE Cart_Items SET quantity = %s WHERE cartItemID = %s"
        execute_query(update_query, (new_quty, existing_item['cartItemID']), fetch="none")
    else:
        insert_query = "INSERT INTO Cart_Items (cartID, plantID, quantity) VALUES (%s, %s, 1)"
        execute_query(insert_query, (cart_id, plant_id), fetch="none")
    
    return redirect(url_for('views.cart'))
    
    

@views.route('/email-confirm-page')
def email_confirm():
    return render_template("emailConfirm.html")

@views.route('/purchase-confirm-page')
def purchase_confirm():
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    return render_template("purchaseConfirm.html", user = user_data)

@views.route('/index')
def index():
    return redirect(url_for("views.login"), 303)
