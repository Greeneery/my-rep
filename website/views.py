from flask import Blueprint, render_template, request, redirect, url_for


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/browse-page')
def browsePage():
    return render_template("browse.html")

@views.route('/contact-page')
def browsePage():
    return render_template("contact.html")

@views.route('/check-out-page')
def browsePage():
    return render_template("checkout.html")

@views.route('/detail-page')
def browsePage():
    return render_template("detail.html")

@views.route('/log-in-page')
def browsePage():
    return render_template("login.html")

@views.route('/sign-up-page')
def browsePage():
    return render_template("signup.html")

@views.route('/favorites-page')
def browsePage():
    return render_template("favorites.html")

@views.route('/cart-page')
def browsePage():
    return render_template("cart.html")

@views.route('/email-confirm-page')
def browsePage():
    return render_template("emailConfirm.html")

@views.route('/purchase-confirm-page')
def browsePage():
    return render_template("purchaseConfirm.html")