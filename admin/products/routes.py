from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from admin import db
from admin.models import Product, Category, SellerPriceList
from admin.products.forms import ProductForm, ProductUpdateForm
from admin.products.utils import save_product
import uuid

product = Blueprint('products',__name__)


@product.route('/newitem',methods=['GET','POST'])
@login_required
def newitem():
    form = ProductForm()
    form.category_id.choices = [('000','None')]+[(i.category_id,i.category_name)for i in Category.query.all()]
    if form.validate_on_submit():
        images = form.image.data
        if images:
            image_file = []
            for data in images:
                path = save_product(data)
                image_file.append(path)
            product_name = SellerPriceList.query.filter_by(id=uuid.UUID(form.product_name.data)).first()
            product = Product(category_id=uuid.UUID(form.category_id.data), seller_id= current_user.seller_id, product_name=product_name.product_name,product_price=product_name.price,
                              product_description=form.description.data,product_quantity=form.quantity.data,product_images=",".join(image_file))
            db.session.add(product)
            db.session.commit()
            flash("Your product request is success wait to your card",'success')
            return redirect(url_for('sellers.seller_home'))
    
    return render_template('seller/newitem.html',form=form)


@product.route('/get_product/<id>',methods=['GET'])
def sellerproduct(id):
     sellerprice = SellerPriceList.query.filter_by(category_id=uuid.UUID(id)).all()
     data = { str(i.id):i.product_name for i in sellerprice }
     return jsonify(data)

@product.route('/get_price/<id>',methods=['GET'])
def sellerprice(id):
     sellerprice = SellerPriceList.query.filter_by(id=uuid.UUID(id)).first()
     return jsonify({'price':sellerprice.price,})


@product.route('/updateitem/<productid>',methods=['GET','POST'])
@login_required
def updateitem(productid):
    form = ProductUpdateForm()
    editproduct = Product.query.filter_by(product_id=uuid.UUID(productid)).first()
    if form.validate_on_submit():
        # editproduct.product_name =form.product_name.data
        # editproduct.product_price =form.price.data
        editproduct.product_description =form.description.data
        editproduct.product_quantity =form.quantity.data
        editproduct.approved_status = "update"
        # if form.image.data:
        #     ProductImage.query.filter_by(product_id=editproduct.product_id).delete()
        #     for data in form.image.data:
        #             path = save_product(data)
        #             product_img = ProductImage(filename=path,product_id=editproduct.product_id)
        #             db.session.add(product_img)
        db.session.commit()
        flash("Your product update request is success wait to your card",'success')
        return redirect(url_for('sellers.seller_home'))
    else:
        form.category_id.data = editproduct.category.category_name
        form.product_name.data = editproduct.product_name
        form.description.data = editproduct.product_description
        form.price.data = editproduct.product_price
        form.quantity.data = editproduct.product_quantity
        image_file = editproduct.product_images
        image_file=image_file.replace('}','')
        image_file = image_file[1:].split(',')
        print(image_file)
        form.image.data = image_file

    return render_template('seller/newitem.html',form=form)
