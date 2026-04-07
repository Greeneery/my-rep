from flask import Flask
from website.views import views
from sql import start_sql_manager, stop_sql_manager, init_database, close_database
import atexit



def create_app():
    app = Flask(__name__, template_folder='template')
    app.config['SECRET_KEY'] = 'T231oL131ove1313RuP1313eakGoAn135757dWat8468chItEls48648eGG48484eF2b3n0p12fcc'
    app.config['DEBUG'] = True

    app.register_blueprint(views, url_prefix='/') 

    with app.app_context():
        # Start SQL manager (FIFO queue worker) and initialize DB
        start_sql_manager()
        init_database()
    
    return app


if __name__ == "__main__":
    app = create_app()
    try:
        app.run(debug=app.config["DEBUG"])
    finally:
        try:
            stop_sql_manager()
        finally:
            close_database()


