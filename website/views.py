from flask import Blueprint, render_template, request, redirect, url_for


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("homePage.html")

@views.route('/browse-page')
def browsePage():
    return render_template("browsePage.html")

@views.route('/contact-page')
def browsePage():
    return render_template("contactPage.html")

@views.route('/check-out-page')
def browsePage():
    return render_template("checkOutPage.html")

@views.route('/detail-page')
def browsePage():
    return render_template("detailPage.html")

@views.route('/log-in-page')
def browsePage():
    return render_template("logInPage.html")

@views.route('/sign-up-page')
def browsePage():
    return render_template("signUpPage.html")

@views.route('/favorites-page')
def browsePage():
    return render_template("favoritesPage.html")

@views.route('/cart-page')
def browsePage():
    return render_template("cartPage.html")

@views.route('/email-confirm-page')
def browsePage():
    return render_template("emailConfirmPage.html")

@views.route('/purchase-confirm-page')
def browsePage():
    return render_template("purchaseConfirmPage.html")