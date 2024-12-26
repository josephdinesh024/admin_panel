from flask import Blueprint,render_template,redirect,url_for,flash,request,jsonify,send_file
from flask_login import login_required,login_user,current_user
from sqlalchemy import or_
from admin import bcrypt, db
from admin.models import Admin, Seller, Product, Category, SellerPriceList, BuyerPriceList
from admin.admins.forms import LoginFrom, NewAdminFrom, CategoryForm, SellerPriceForm, UpdateSellerPriceForm
from admin.admins.utils import save_product, create_pdf


admin = Blueprint('admins',__name__)

@admin.route('/admin')
@login_required
def adminsite():
    if isinstance(current_user,Seller):
        return redirect(url_for('sellers.seller_home'))
    else:
        sellerrequest = Seller.query.filter_by(approved_status='pending').all()
        productrequest = Product.query.filter( or_(Product.approved_status=='pending',Product.approved_status=='update')).all()
        seller = Seller
        product = Product
        print(productrequest)
        return render_template("admin/adminsite.html",requests=sellerrequest,prequests=productrequest,seller=seller,product=product)


@admin.route('/admin/login',methods=['GET','POST'])
def login():
    forms = LoginFrom()
    if forms.validate_on_submit():
        admins = Admin.query.filter_by(email_id=forms.email.data).first()
        if admins and bcrypt.check_password_hash(admins.password,forms.password.data):
            login_user(admins)
            flash(f"Login success with {admins.admin_name} ",'success')
            #next = request.args.get('next')
            return redirect(url_for('admins.adminsite')) #redirect(next) if next else redirect(url_for('index'))
        else:
            flash(f"Username or Password incoorect ",'danger')
    return render_template('admin/adminlogin.html',forms=forms)

@admin.route("/admin_profile")
def admin_profile():
    admin = Admin.query.filter_by(admin_id=current_user.admin_id).first()
    return render_template("admin/profile.html",admin=admin)


@admin.route("/admin/addadmin",methods=['GET','POST'])
@login_required
def addadmin():
    if not Admin.query.filter_by(admin_name=current_user.admin_name,admin_role='superadmin').first():
        flash('Permission refused to add admin','danger')
        return redirect(url_for('admins.adminsite'))
    forms = NewAdminFrom()
    if forms.validate_on_submit():
        admins = Admin(admin_name=forms.username.data,email_id=forms.email.data,
                       password=bcrypt.generate_password_hash(forms.password.data).decode('utf-8'))#,admin_role='superadmin')
        db.session.add(admins)
        db.session.commit()
        flash('Admin created successfully','success')
        return redirect(url_for('admins.adminsite'))
    return render_template('admin/addadmin.html',forms=forms)
    
@admin.route('/admin/seller')
@login_required
def adminsite_seller():
    if isinstance(current_user,Seller):
        return redirect(url_for('seller.home'))
    else:
        sellerrequest = Seller.query.all()            
        return render_template("admin/adminseller.html",requests=sellerrequest)
    
@admin.route('/admin/product')
@login_required
def adminsite_product():
    if isinstance(current_user,Seller):
        return redirect(url_for('seller.home'))
    sellerid = request.args.get('sellerid')
    if sellerid:
        productrequest = Product.query.filter_by(seller_id=sellerid)
    else:
        # print(datetime.datetime.now())
        productrequest = Product.query.all()  
    return render_template("admin/adminproduct.html",requests=productrequest)

@admin.route('/admin/requestform')
@login_required
def requestform():
    if isinstance(current_user,Seller):
            return redirect(url_for('seller.home'))
    else:
        request_id = request.args.get('request_id')
        action = request.args.get('action')
        if Seller.query.filter_by(seller_id=request_id).first():
            request_data = Seller.query.filter_by(seller_id=request_id).first()
            if action == 'approve':
                request_data.approved_status = 'approved'
                request_data.admin_id = current_user.admin_id
                db.session.commit()
                return redirect(url_for('admins.adminsite'))
            elif action == 'reject':
                request_data.approved_status = 'reject'
                request_data.admin_id = current_user.admin_id
                db.session.commit()
                return redirect(url_for('admins.adminsite'))
        else:
            request_data = Product.query.filter_by(product_id=request_id).first()

            if action == 'approve':
                request_data.approved_status = 'approved'
                request_data.admin_id = current_user.admin_id
                db.session.commit()
                return redirect(url_for('admins.adminsite'))
            elif action == 'reject':
                request_data.approved_status = 'reject'
                request_data.admin_id = current_user.admin_id
                db.session.commit()
                return redirect(url_for('admins.adminsite'))
        return render_template('admin/requestform.html',data=request_data)

@admin.route('/add_image/<id>',methods=['GET','POST'])
def update_product(id):
    image_list = request.form.get('imagelist')
    product_discription = request.form.get('update_product_description')
    new_image = request.files
    image_list = image_list.split(',')
    print('new image',image_list)
    if new_image.get('image'):
        for img in list(new_image.listvalues())[0]:
            path = save_product(img)
            image_list.append(path)
    print(image_list)
    product = Product.query.filter_by(product_id=id).first()
    product.product_description = product_discription
    product.product_images = image_list
    db.session.commit()
    flash("Product Updated",'success')
    print(id)
    return redirect(url_for('admins.requestform',request_id=id))

@admin.route('/admin/category',methods=['GET','POST'])
@login_required
def category():
    form = CategoryForm()
    form.category_id.choices = [('000','None')]+[(i.category_id,i.category_name)for i in Category.query.all()]
    print(form.category_id.choices)
    if form.validate_on_submit():
        addcategory = Category(category_name=form.name.data)
        db.session.add(addcategory)
        db.session.commit()
        flash('New Category add successfully','success')
        return redirect(url_for('admins.adminsite'))
    return render_template('admin/category.html',form=form)

@admin.route('/admin/sellerprice',methods=['GET','POST'])
@login_required
def sellerprice():
    seller_price = SellerPriceList.query.all()
    action = request.args.get('action','')
    print(request.method)

    if action=='update':
        print('method get')
        update_price = request.args.get('update_price')
        price = SellerPriceList.query.filter_by(id=update_price).first()
        form = UpdateSellerPriceForm()
        form.category.data = price.category.category_name
        form.name.data = price.product_name
        if form.validate_on_submit():
            price.price = form.price.data
            db.session.commit()
            flash('Price as been updated','success')
            return redirect(url_for('admins.sellerprice'))
        return render_template('admin/sellerprice.html',form=form,seller_price=seller_price)
    
    elif action=='add':
        form = SellerPriceForm()
        form.category.choices = [('000','None')]+[(i.category_id,i.category_name)for i in Category.query.all()]
        if form.validate_on_submit():
            new_price = SellerPriceList(category_id=form.category.data,product_name=form.name.data,
                                        price=form.price.data,admin_id=current_user.admin_id)
            db.session.add(new_price)
            db.session.commit()
            flash('New Product price added','success')
            return redirect(url_for('admins.sellerprice'))
        return render_template('admin/sellerprice.html',form=form,seller_price=seller_price)
    
    return render_template('admin/sellerprice.html',seller_price=seller_price)

@admin.route('/admin/cartprice',methods=['GET','POST'])
def cart_price():
    product = Product.query.filter_by(approved_status='approved').all()
    product_id =request.args.get('product_id')
    form = request.form
    print(form)
    if product_id and form:
        cart_price = BuyerPriceList.query.filter_by(product_id=product_id).first()
        if cart_price:
            print(cart_price.price)
            cart_price.price = form.get('cart_price',type=int)
            flash('Cart price updated','success')
        else:
            selected_product = Product.query.filter_by(product_id=product_id).first()
            new_price = BuyerPriceList(product_id=product_id,product_name=selected_product.product_name,price=form.get('cart_price',type=int))
            db.session.add(new_price)
            flash('New Cart price added','success')
        db.session.commit()
        return redirect(url_for('admins.cart_price'))
    return render_template('admin/cart_price.html',products=product)

@admin.route('/edit_cart_price/<id>')
def edit_cart_price(id):
    product = Product.query.filter_by(product_id=id).first()
    price = product.cart_price[0].price if product.cart_price else 0
    data = {'name':product.product_name,
            'price':round(price)}
    return jsonify(data)

@admin.route('/menu')
def menu():
    return render_template('admin/menu.html')

@admin.route('/admin/report', methods=['GET', 'POST'])
def report():
    seller = request.form.get('seller')
    product = request.form.get('product')

    data = {}

    if seller == 'on':
        start_date = request.form.get('seller_start_date')
        end_date = request.form.get('seller_end_date')
        if start_date and end_date:
        # # Query your database for products/sellers within the date range
        # products = Product.query.filter(Product.date >= start_date, Product.date <= end_date).all()
            sellers = Seller.query.filter(Seller.updated_date >= start_date, Seller.updated_date <= end_date).all()
            data['seller'] = sellers
    
    if product == 'on':
        start_date = request.form.get('product_start_date')
        end_date = request.form.get('product_end_date')
        if start_date and end_date:
        # # Query your database for products/sellers within the date range
            products = Product.query.filter(Product.updated_date >= start_date, Product.updated_date <= end_date).all()
            data['product'] = products
            # sellers = Seller.query.filter(Seller.updated_date >= start_date, Seller.updated_date <= end_date).all()
        # # Create PDF report
    if request.method == 'POST' and data:
        return create_pdf(data)
    return render_template('admin/report.html')


 