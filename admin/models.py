import random, datetime
from admin import db,login_manager, app
import uuid
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(id):
    # For Admin login
    admin = Admin.query.get(id)
    if admin:
        return admin
    # For Seller login
    seller =  Seller.query.get(id)
    if seller:
        return seller
    return User.query.get(id)

class User(db.Model,UserMixin):
    __bind_key__ = 'testdb'
    __tablename__ = 'users'
        
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    #password_hash = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20),unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f"User({self.name},{self.email},{self.phone},{self.updated_at})"
    
    def get_id(self):
        return str(self.user_id)

    

class Address(db.Model):
    __bind_key__ = 'testdb'
    __tablename__ = 'addresses'

    address_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'))
    street = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    #type = db.Column(db.String(50))  # e.g., Home, Office

    user = db.relationship('User', backref=db.backref('addresses', lazy=True,cascade='all, delete-orphan'))

    def __repr__(self):
        return f"Address({self.street},{self.city},{self.state},{self.postal_code})"
    

class Admin(db.Model,UserMixin):
    __tablename__ = "admin_info"
    admin_id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    admin_role = db.Column(db.String(100),nullable=False,default='moderator')    #'superadmin', 'moderator', etc.
    admin_name = db.Column(db.String(100),nullable=False)
    email_id = db.Column(db.String(250),nullable=False,unique=True)
    password = db.Column(db.String(250),nullable=False)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_date = db.Column(db.DateTime, nullable=True)

    def get_id(self):
        return str(self.admin_id)
    

class Seller(db.Model,UserMixin):
    __tablename__ = "seller_info"
    seller_id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    seller_name = db.Column(db.String(100),nullable=False)
    email_id = db.Column(db.String(250),nullable=False,unique=True)
    email_verification = db.Column(db.Boolean,default=False)
    mobile_number = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(200),nullable=False)
    company_name = db.Column(db.String(200),nullable=False)
    street = db.Column(db.Text,nullable=False)
    city = db.Column(db.String(100),nullable=False)
    state = db.Column(db.String(100),nullable=False)
    postal_code = db.Column(db.String(20),nullable=False)
    country = db.Column(db.String(100),nullable=False)
    document_copy = db.Column(db.Text,nullable=False)  # Photo Document
    company_description = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    approved_status = db.Column(db.String(50),nullable=False,default='pending')   # Approved or Reject
    admin_id = db.Column(UUID(as_uuid=True),db.ForeignKey('admin_info.admin_id'))
    deleted_date = db.Column(db.DateTime, nullable=True)

    def get_id(self):
        return str(self.seller_id)
    
    def reset_token(self,times=1800):
        otp = random.randint(1000,9999)
        s = Serializer(app.config['SECRET_KEY'],times)
        return s.dumps({'sellerid':str(self.seller_id),'otp':otp}).decode('utf-8')
    
    @staticmethod
    def verify(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            sellerid = s.loads(token)['sellerid']
        except:
            return None
        return Seller.query.filter_by(seller_id=sellerid).first()

# class SellerAddress(db.Model):
#     __tablename__ = "addresses"
#     address_id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
#     seller_id = db.Column(UUID(as_uuid=True),db.ForeignKey('sellers.seller_id'))
    
#     status = db.Column(db.String(50),nullable=False,default='pending')  #reject or approved
#     seller = db.relationship('Seller',backref=db.backref('address',lazy=True,cascade='all, delete-orphan'))
class BuyerPriceList(db.Model):
    __tablename__ = 'buyer_price'
    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    product_id = db.Column(UUID(as_uuid=True),db.ForeignKey('products.product_id'))
    category_id = db.Column(UUID(as_uuid=True),db.ForeignKey('categories.category_id'))
    product_name = db.Column(db.String(255))
    category_name = db.Column(db.String(255))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_date = db.Column(db.DateTime, nullable=True)
    admin_id = db.Column(UUID(as_uuid=True),db.ForeignKey('admin_info.admin_id'))
    product =db.relationship('Product',backref=db.backref('cart_price',lazy=True,cascade="all,delete-orphan"))

class SellerPriceList(db.Model):
    __tablename__ = 'seller_price'
    id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('categories.category_id'))
    product_name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_date = db.Column(db.DateTime, nullable=True)
    admin_id = db.Column(UUID(as_uuid=True),db.ForeignKey('admin_info.admin_id'))
    category = db.relationship('Category', backref=db.backref('sellerprice', lazy=True,cascade='all, delete-orphan'))
    def __repr__(self):
        return f"Seller_price({self.product_name},{self.price})"

class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_name = db.Column(db.String(255), nullable=False)
    display = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_date = db.Column(db.DateTime, nullable=True)
    parent_category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('categories.category_id'))                   
    parent_category = db.relationship('Category', remote_side=[category_id],backref=db.backref('subcategories'))
    admin_id = db.Column(UUID(as_uuid=True),db.ForeignKey('admin_info.admin_id'))

    def __repr__(self):
        return f"Category({self.category_id},{self.category_name})"
    
class Product(db.Model):
    __tablename__ = "products"
    product_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seller_id = db.Column(UUID(as_uuid=True), db.ForeignKey('seller_info.seller_id'))
    product_name = db.Column(db.String(255), nullable=False)
    product_description = db.Column(db.Text)
    product_price = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('categories.category_id'))
    product_quantity = db.Column(db.Integer, default=0)
    product_images = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    deleted_date = db.Column(db.DateTime, nullable=True)
    approved_status = db.Column(db.String(50),nullable=False,default='pending')
    seller = db.relationship('Seller',backref=db.backref('product',lazy=True,cascade='all, delete-orphan'))
    category = db.relationship('Category', backref=db.backref('products', lazy=True,cascade='all, delete-orphan'))
    admin_id = db.Column(UUID(as_uuid=True),db.ForeignKey('admin_info.admin_id'))

    def soft_delete(self):
        self.deleted_date = datetime.datetime.now(datetime.UTC)
        db.session.commit()

# class ProductImage(db.Model):
#     __tablename__ = "productimages"
#     image_id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
#     filename = db.Column(db.Text,nullable=False)
#     product_id = db.Column(UUID(as_uuid=True),db.ForeignKey('products.product_id'),nullable=False)
#     product = db.relationship('Product',backref=db.backref('images',lazy=True,cascade='all, delete-orphan'))

# class SellerRequest(db.Model):
#     __tablename__ = "sellerrequest"
#     request_id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
#     seller_id = db.Column(UUID(as_uuid=True), db.ForeignKey('sellers.seller_id'))
#     status = db.Column(db.String(50),nullable=False,default='pending')
#     note = db.Column(db.Text)
#     admin_id = db.Column(UUID(as_uuid=True),db.ForeignKey('admins.admin_id'))
#     seller = db.relationship('Seller',backref=db.backref('seller_detail',lazy=True))

# class ProductRequest(db.Model):
#     __tablename__ = "productrequset"
#     request_id = db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
#     product_id = db.Column(UUID(as_uuid=True),db.ForeignKey('products.product_id'))
#     seller_id = db.Column(UUID(as_uuid=True),db.ForeignKey('sellers.seller_id'))
#     status = db.Column(db.String(50),nullable=False,default='pending')
#     note = db.Column(db.Text)
#     admin_id = db.Column(UUID(as_uuid=True),db.ForeignKey('admins.admin_id'))

# class Order(db.Model):
#     __bind_key__ = 'testdb'
#     __tablename__ = 'orders'
        
#     order_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'))
#     order_date = db.Column(db.DateTime, default=db.func.current_timestamp())
#     status = db.Column(db.String(50), default='Pending')
#     total_amount = db.Column(db.Numeric(10, 2), nullable=False)
#     shipping_address_id = db.Column(UUID(as_uuid=True), db.ForeignKey('addresses.address_id'))
#     billing_address_id = db.Column(UUID(as_uuid=True), db.ForeignKey('sellers.seller_id'))
    
#     user = db.relationship('User', backref=db.backref('orders', lazy=True))
#     shipping_address = db.relationship('Address', foreign_keys=[shipping_address_id])
#     billing_address = db.relationship('Seller', foreign_keys=[billing_address_id])

# class OrderItem(db.Model):
#     __bind_key__ = 'testdb'
#     __tablename__ = 'orderitems'
    
#     order_item_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     order_id = db.Column(UUID(as_uuid=True), db.ForeignKey('orders.order_id'))
#     product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('products.product_id'))
#     quantity = db.Column(db.Integer, nullable=False)
#     price_at_purchase = db.Column(db.Numeric(10, 2), nullable=False)

#     order = db.relationship('Order', backref=db.backref('order_items', lazy=True))
#     product = db.relationship('Product', backref=db.backref('order_items', lazy=True))

#     def __repr__(self):
#         return f"OrderItem({self.product_id},{self.quantity},{self.price_at_purchase})"
    
    