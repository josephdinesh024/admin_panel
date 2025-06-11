from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, logout_user, login_required
from admin import db
from admin.models import Category, Product, User
from admin.main.forms import BuyForm

main = Blueprint('mains',__name__)

@main.route("/")
def index():
    if current_user.is_authenticated:
        print("yes")
        # u= User.query.filter_by(phone = current_user.phone).first()
        # print(u.addresses)
        # db.session.delete(u)
        # db.session.commit()
    return render_template("index.html")

@main.route("/category",methods=['GET','POST'])
def category():
    categorys = Category.query.all()
    # if request.method == 'POST':
    #     names = request.form.get('names')
    #     print(names)
    #     new_name = Category(name=names)
    #     db.session.add(new_name)
    #     db.session.commit()
    return render_template("category.html",categorys=categorys)


@main.route("/categorylist")
def category_list():
    category_id = request.args.get('category_id','0',str)
    try:
        products = Product.query.filter_by(category_id=category_id,approved_status='approved').all()
        return render_template("category_list.html",products=products)
    except:
        flash(f"No data found",'warning')
        return redirect("category")

@main.route("/buyform",methods=['GET','POST'])
@login_required
def buyform():
    form = BuyForm()
    product_id = request.args.get('product_id',type=str)
    select_product = Product.query.filter_by(product_id=product_id).first()
    print(select_product)
    if form.validate_on_submit():
        # shipping = Address.query.filter_by(user_id=current_user.user_id).first()
        # products = Product.query.filter_by(product_id=form.product_id.data).first()
        # products.stock_quantity -= form.quantity.data
        # add_order = Order(user_id=current_user.user_id,total_amount=(form.quantity.data*products.price),
        #                   shipping_address_id=shipping.address_id,billing_address_id=products.Seller_id)
        # db.session.add(products)
        # db.session.add(add_order)
        # db.session.commit()
        # product = Order.query.order_by(Order.order_date.desc()).filter_by(user_id=current_user.user_id,total_amount=(form.quantity.data*products.price)).first()
        # add_orderitem = OrderItem(order_id =product.order_id ,product_id=form.product_id.data,quantity=form.quantity.data,
        #                          price_at_purchase=form.purchase_price.data)
        # db.session.add(add_orderitem)
        # db.session.commit()
        return redirect(url_for("index"))
    return render_template("buyform.html",form=form,select_product=select_product)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('mains.index'))