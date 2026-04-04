from flask import Blueprint, render_template, request, redirect, url_for


views = Blueprint('views', __name__, template_folder="template")

@views.route('/')
def home():
    return render_template("home.html")

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
