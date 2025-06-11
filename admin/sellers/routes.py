import random, uuid
from flask import Blueprint,render_template,redirect,url_for,flash,request
from flask_login import login_user, current_user, login_required
from admin import bcrypt, db, app
from admin.models import Seller, Admin, Product, User
from admin.sellers.forms import LoginFrom, SellerForm
from admin.sellers.utils import save_document, send_otp_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

seller = Blueprint('sellers',__name__)

@seller.route('/seller')
@login_required
def seller_home():
    if isinstance(current_user,Admin):
        return redirect(url_for('admins.adminsite'))
    if isinstance(current_user,User):
        return redirect(url_for('mains.index'))
    if current_user.is_authenticated:
        products = Product.query.order_by(Product.product_name).filter_by(seller_id=current_user.seller_id)
        return render_template('seller/home.html',products=products)
    return render_template('seller/home.html')


@seller.route('/seller/login',methods=['GET','POST'])
def login():
    forms = LoginFrom()
    if forms.validate_on_submit():
        seller = Seller.query.filter_by(email_id=forms.email.data).first()
        if seller and bcrypt.check_password_hash(seller.password,forms.password.data):
            state = seller.email_verification
            if not state:
                otp = random.randint(1000,9999)
                data = dict(email=seller.email_id,otp=otp)
                s = Serializer(app.config['SECRET_KEY'],1800)
                send_otp_mail(data)
                return redirect(f"otp/{s.dumps(data).decode('utf-8')}/{str(seller.seller_id)}")
            
            elif seller.approved_status =='approved':
                login_user(seller)
                flash(f"Login success with {seller.seller_name} ",'success')
                #next = request.args.get('next')
                return redirect(url_for('sellers.seller_home')) #redirect(next) if next else redirect(url_for('index'))
            
            else:
                flash(f'Wait for Status update. Current status "{seller.approved_status}" ','info')
                return redirect(url_for('sellers.seller_home'))
        else:
            flash(f"Username or Password incoorect ",'danger')
    return render_template('seller/login.html',forms=forms)


@seller.route("/seller/register",methods=['GET','POST'])
def registration():
    forms = SellerForm()
    if forms.validate_on_submit() and forms.document.data:
        filepath = save_document(forms.document.data)
        seller = Seller(seller_name=forms.username.data,email_id=forms.email.data,mobile_number=forms.phone.data,
                        password=bcrypt.generate_password_hash(forms.password.data).decode('utf-8'),company_name=forms.factory_name.data,street=forms.street.data,city=forms.city.data,
                              state=forms.state.data,postal_code=forms.postal_code.data,country=forms.country.data,
                              document_copy=filepath,company_description=forms.description.data)
        db.session.add(seller)
        db.session.commit()

        otp = random.randint(1000,9999)
        data = dict(email=forms.email.data,otp=otp)
        s = Serializer(app.config['SECRET_KEY'],1800)
        send_otp_mail(data)
        return redirect(f"otp/{s.dumps(data).decode('utf-8')}/{seller.seller_id}")

    return render_template('seller/seller_register.html',form=forms)

@seller.route("/seller/otp/<token>/<id>",methods=['GET','POST'])
def otp_verify(token,id):
    # token = request.args.get('token')
    s = Serializer(app.config['SECRET_KEY'])
    error = ''
    email = ''
    
    seller = Seller.query.filter_by(seller_id=uuid.UUID(id)).first()
    print(id,type(id),seller)
    try:
        data= s.loads(token)
        email = data.get('email')                                      
    except:
        flash("Token as expired or invalied",'info')

    else:
        if data.get('otp') == request.form.get('otp',type=int) and data.get('email') == seller.email_id:
                seller.email_verification = True
                db.session.commit()
                return redirect(url_for('sellers.login'))
        elif data.get('otp') != request.form.get('otp',type=int) and request.form.get('otp',type=int) != None:
            error='Invalied otp'

    return render_template('seller/email.html',error=error,email=email)

@seller.route("/seller_profile")
def seller_profile():
    seller = Seller.query.filter_by(seller_id=current_user.seller_id).first()
    return render_template("seller/profile.html",seller=seller)

@seller.route('/get_product_decending')
@login_required
def product_decending():
    if isinstance(current_user,Admin):
        return redirect(url_for('admins.adminsite'))
    if isinstance(current_user,User):
        return redirect(url_for('mains.index'))
    if current_user.is_authenticated:
        products = Product.query.order_by(Product.product_name.desc()).filter_by(seller_id=current_user.seller_id)
        print(products)
    return render_template('seller/home.html',products=products,selected=1)

@seller.route('/get_price_decending')
@login_required
def price_decending():
    if current_user.is_authenticated:
        products = Product.query.order_by(Product.product_price.desc()).filter_by(seller_id=current_user.seller_id)
        print(products)
    return render_template('seller/home.html',products=products,selected=3)

@seller.route('/get_price_ascending')
@login_required
def price_ascending():
    if current_user.is_authenticated:
        products = Product.query.order_by(Product.product_price).filter_by(seller_id=current_user.seller_id)
        print(products)
    return render_template('seller/home.html',products=products,selected=2)

@seller.route('/get_status_approved')
@login_required
def status_approved():
    if current_user.is_authenticated:
        products = Product.query.filter_by(seller_id=current_user.seller_id,approved_status='approved')
        print(products)
    return render_template('seller/home.html',products=products,selected=4)

@seller.route('/get_status_pending')
@login_required
def status_pending():
    if current_user.is_authenticated:
        products = Product.query.filter(Product.approved_status!='approved').filter_by(seller_id=current_user.seller_id)
        print(products)
    return render_template('seller/home.html',products=products,selected=5)


#@seller.route("/address",methods=['GET','POST']) 
# def address():
#     form = SellerAddressForm()
#     sellerid =request.args.get('sellerid')
#     if not sellerid:
#         return redirect(url_for('sellers.seller'))
#     if form.validate_on_submit():
#         address = Seller(seller_id=sellerid)
#         db.session.add(address)
#         db.session.commit()
#         flash(f'Request as generated wait for approvel','success')
#         return redirect(url_for('home'))
#     return render_template('seller/address.html',aform=form)
