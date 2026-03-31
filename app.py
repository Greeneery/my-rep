from flask import Flask
from website.views import views
from sql import start_sql_manager, stop_sql_manager, init_database, close_database
import atexit



def create_app():
    app = Flask(__name__, template_folder='template')
    app.config['SECRET_KEY'] = 'aaaaaaaa'

    app.register_blueprint(views, url_prefix='/') 

    start_sql_manager()
    init_database()
    atexit.register(stop_sql_manager)
    
    return app

app = create_app()

if __name__ == "__main__":
    app = create_app()
    try:
        app.run(debug=app.config["DEBUG"])
    finally:
        try:
            stop_sql_manager()
        finally:
            close_database()


