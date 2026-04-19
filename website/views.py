from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, SignupForm
import models
import auth
from sql import execute_query
from auth import login_required
from decimal import Decimal



views = Blueprint('views', __name__, template_folder="template")

VALID_CODE = {
    'FREETHEDEV': 0.2, 'SUS404': 10.00 , 'WELCOME10': 0.1
}

@views.route('/')
def home():
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    
    random_query = "SELECT * FROM Plants ORDER BY RAND() LIMIT 12"
    featured_plants = execute_query(random_query, fetch="all")
    
    sus_query = "SELECT * FROM Plants ORDER BY plantID DESC LIMIT 10"
    sus_plants = execute_query(sus_query, fetch="all")
    
    low_qty_query = "SELECT * FROM Plants WHERE stockQuantity <= 10 ORDER BY stockQuantity ASC"
    low_qty_plants = execute_query(low_qty_query, fetch="all")
    
    return render_template("home.html", user = user_data, featured_plants=featured_plants, sus_plants = sus_plants, low_qty_plants= low_qty_plants)

@views.route('/browse-page')
def browse():
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    
    user_favorites = []
    
    if user_data:
        fav_data = models.Favorites.get_user_favorites(user_data['user_id'])
        user_favorites = [fav['plantID'] for fav in fav_data] #type: ignore
    
    lowLightFilter = request.args.get('llight')
    mediumLightFilter = request.args.get('mlight')
    biLightFilter = request.args.get('bilight')
    dsLightFilter = request.args.get('dslight')
    smallPlantFilter = request.args.get('ssize')
    mediumPlantFilter = request.args.get('msize')
    largePlantFilter = request.args.get('lsize')
    ultraLargePlantFilter = request.args.get('ulsize')
    airPurifierFilter = request.args.get('air')
    petFriendlyFilter = request.args.get('pet')
    
    query = "SELECT * FROM Plants WHERE 1=1"
    params = []
    
    if lowLightFilter == 'Low':
        query += " AND lightRequirement = %s"
        params.append('Low')
        
    if mediumLightFilter == 'Medium':
        query += " AND lightRequirement = %s"
        params.append('Medium')
        
    if biLightFilter == 'Bright Indirect':
        query += " AND lightRequirement = %s"
        params.append('Bright Indirect')
        
    if dsLightFilter == 'Direct Sunlight':
        query += " AND lightRequirement = %s"
        params.append('Direct Sunlight')
    
    if smallPlantFilter == 'Small':
        query += " AND plantSize = %s"
        params.append('Small')
        
    if mediumPlantFilter == 'Medium':
        query += " AND plantSize = %s"
        params.append('Medium')
        
    if largePlantFilter == 'Large':
        query += " AND plantSize = %s"
        params.append('Large')
    
    if ultraLargePlantFilter == 'Ultra Large':
        query += " AND plantSize = %s"
        params.append('Ultra Large')
        
    if airPurifierFilter == '1':
        query += " AND isAirCleaner = %s"
        params.append('1')
        
    if petFriendlyFilter == '1':
        query += " AND isPetFriendly = %s"
        params.append('1')
        
    real_plants = execute_query(query, tuple(params), fetch="all")
        
    return render_template("browse.html", user = user_data, plants = real_plants, user_favorites=user_favorites)

@views.route('/contact-page')
def contact():
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    return render_template("contact.html", user = user_data)

@views.route('/check-out-page')
@login_required
def checkout():
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    
    if user_data is None:
        return redirect(url_for('views.login'))
    
    full_user = models.UserBase.get_by_id(user_data['user_id'])
    
    cart_id = models.Cart.get_or_create_cart(user_data['user_id'])
    items = models.Cart.get_items_with_details(cart_id)
    
    subtotal = sum(item['price'] * item['quantity'] for item in items) #type: ignore
    discount_amnt = 0
    if 'discount_code' in session:
        discount_val = session['discount_value']
        
        if discount_val < 1:
            discount_amnt = subtotal * Decimal(discount_val)
        else:
            discount_amnt = Decimal(discount_val)
            
    total = max(0, subtotal - discount_amnt)
      
    return render_template("checkout.html", user = full_user.to_dict(), total = total, items=items, subtotal=subtotal, discount_amount=discount_amnt) #type: ignore

@views.route('/process-checkout', methods=['POST'])
@login_required
def process_checkout():
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    
    if user_data is None:
        return redirect(url_for('views.login'))
    
    user_id = user_data['user_id']
    
    cart_id = models.Cart.get_or_create_cart(user_id)
    items = models.Cart.get_items_with_details(cart_id)
    
    if not items:
        return redirect(url_for('views.cart'))
    
    for item in items:
        update_quantity = "UPDATE Plants SET stockQuantity = stockQuantity - %s WHERE plantID = %s"
        execute_query(update_quantity, (item['quantity'], item['plantID']), fetch="none")
        
    session.pop('discount_code', None)
    session.pop('discount_value', None)
        
    clear_cart = "DELETE FROM Cart_items WHERE cartID = %s"
    execute_query(clear_cart, (cart_id,), fetch="none")
  
    flash(f'Order placed successfully! >:3', category="success")
    return redirect(url_for('views.purchase_confirm'))
    

@views.route('/detail-page/<int:plant_id>')
def detail(plant_id):
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    
    user_favorites = []
    
    if user_data:
        fav_data = models.Favorites.get_user_favorites(user_data['user_id'])
        user_favorites = [fav['plantID'] for fav in fav_data] #type: ignore
    
    plant = None
    
    try:
        from sql import execute_query
        # Fetch plant from database
        query = "SELECT * FROM Plants WHERE plantID = %s"
        plant = execute_query(query, (plant_id,), fetch="one")
    except Exception as e:
        print(f"Database error: {e}")
        plant = None
        
    return render_template("detail.html", user =user_data, plant = plant, user_favorites=user_favorites)

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
@login_required
def favorites():
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    
    if user_data is None:
        return redirect(url_for('views.login'))
    
    favorite_plants = models.Favorites.get_user_favorites(user_data['user_id'])
    
    print("FAVORITES FOUND:", favorite_plants)
    
    return render_template("favorites.html", user = user_data, favorites = favorite_plants)

@views.route('/toggle-favorite/<int:plant_id>', methods=['POST'])
def toggle_fav(plant_id):
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    
    if user_data is None:
        return redirect(url_for('views.login'))
    
    status = models.Favorites.toggle_favorites(user_data['user_id'], plant_id)
    
    if "added" in status:
        flash("Added this plant to your favorite page! ;3", category="success")
    else:
        flash("Removed this plant from your favorite page! >:3", category="info")
    
    return redirect(request.referrer or url_for('views.favorites'))
    

@views.route('/cart-page')
@login_required
def cart():
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    
    if user_data is None:
        return redirect(url_for('views.login'))
    
    cart_id = models.Cart.get_or_create_cart(user_data['user_id'])
    items = models.Cart.get_items_with_details(cart_id)
    
    total = sum(item['price'] * item['quantity'] for item in items) if items else 0
        
    return render_template("cart.html", user = user_data, items = items, total = total)

@views.route('/add-to-cart/<int:plant_id>', methods=['POST'])
def add_to_cart(plant_id):
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    
    if user_data is None:
        return redirect(url_for('views.login'))
    
    user_id = user_data['user_id']
    cart_id = models.Cart.get_or_create_cart(user_id)
    
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

@views.route('/remove-from-cart/<int:cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    
    delete_query = "DELETE FROM Cart_Items WHERE cartItemID = %s"
    execute_query(delete_query, (cart_item_id,), fetch="none")
    
    return redirect(url_for('views.cart'))

@views.route('/update-cart/<int:cart_item_id>/<action>', methods=['POST'])
@login_required
def update_cart(cart_item_id, action):
    token = request.cookies.get("auth_token")
    user_data, error = auth.verify_token(token)
    
    check_query = "SELECT quantity FROM Cart_Items WHERE cartItemID = %s"
    item = execute_query(check_query, (cart_item_id,), fetch="one")
    
    if item:
        current_quantity = item['quantity']
        
        if action == 'increase':
            new_quantity = current_quantity + 1
            update_query = "UPDATE Cart_Items SET quantity = %s WHERE cartItemID = %s"
            execute_query(update_query, (new_quantity, cart_item_id), fetch="none")
        elif action == 'decrease':
            new_quantity = current_quantity - 1
            if new_quantity > 0:
                update_query = "UPDATE Cart_Items SET quantity = %s WHERE cartItemID = %s"
                execute_query(update_query, (new_quantity, cart_item_id), fetch="none")
            else:
                delete_query = "DELETE FROM Cart_Items WHERE cartItemID = %s"
                execute_query(delete_query, (cart_item_id,), fetch="none")
    
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
    return redirect(url_for("views.home"), 303)

@views.route('/apply-discount', methods=['POST'])
def apply_discount():
    discount_code = request.form.get('discount_code').strip().upper() # type: ignore
    
    if discount_code in VALID_CODE:
        session['discount_code'] = discount_code
        session['discount_value'] = VALID_CODE[discount_code]
        flash(f'A! Discount applied >;3 Enjoy!', category='success')
    else:
        flash(f'Invalid code! LOL! Try again bruv :P', category='error')
        
    return redirect(url_for('views.checkout'))
    


