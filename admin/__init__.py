from flask import Flask,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
app = Flask(__name__)

app.config['SECRET_KEY'] = '323jjvfhiKISHDIH38u0HBIW3DIHbhsdbihidi'
DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user='postgres',pw='Victus',url='localhost',db='admindb')
DB_URL2 = 'postgresql://{user}:{pw}@{url}/{db}'.format(user='postgres',pw='Victus',url='localhost',db='testdb')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_BINDS'] = {
    'testdb': DB_URL2  # Secondary database
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
@login_manager.unauthorized_handler
def handle_unauthorized():
    # Check if the user is trying to access a seller or admin page
    if request.path.startswith('/seller'):
        # Redirect to seller login page
        return redirect(url_for('sellers.login', next=request.url))
    elif request.path.startswith('/admin'):
        # Redirect to admin login page
        return redirect(url_for('admins.login', next=request.url))
    else:
        # General fallback (you can customize this)
        return redirect(url_for('users.login'))


app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Mail server
app.config['MAIL_PORT'] = 587  # Mail server port
app.config['MAIL_USE_TLS'] = True  # Enable Transport Layer Security (TLS)
app.config['MAIL_USERNAME'] = 'dineshckv2003@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'xorqjmyiatfaisjr'
mail = Mail(app)

migrate = Migrate(app, db)

from admin.main.routes import main
from admin.admins.routes import admin
from admin.sellers.routes import seller
from admin.products.routes import product
from admin.users.routes import user

app.register_blueprint(main)
app.register_blueprint(admin)
app.register_blueprint(seller)
app.register_blueprint(product)
app.register_blueprint(user)

