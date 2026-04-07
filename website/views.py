from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, SignupForm
import models
import auth
from sql import execute_query


views = Blueprint('views', __name__, template_folder="template")

@views.route('/')
def home():
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    return render_template("home.html", user = user_data)

@views.route('/browse-page')
def browse():
    return render_template("browse.html")

@views.route('/contact-page')
def contact():
    return render_template("contact.html")

@views.route('/check-out-page')
def checkout():
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

@views.route('/index')
def index():
    return redirect(url_for("views.login"), 303)
