from flask_wtf import FlaskForm
import uuid
from wtforms import StringField, EmailField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from admin.models import Admin, Category, SellerPriceList

class LoginFrom(FlaskForm):
    email = EmailField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')

class NewAdminFrom(FlaskForm):
    #role = StringField('Role',validators=[DataRequired()])
    username = StringField('Admin Name',validators=[DataRequired(),Length(min=3)])
    email = EmailField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    conform_password = PasswordField('Conform Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Create')

    def validate_email(self,email):
        admin = Admin.query.filter_by(email_id=email.data).first()
        if admin:
            raise ValidationError("The email already exist. Try another")
        
class CategoryForm(FlaskForm):
    category_id = SelectField('Category',choices=[])
    name  = StringField('Category Name ',validators=[DataRequired()])
    submit = SubmitField('Add')
         
class SellerPriceForm(FlaskForm):
    category = SelectField('Category',choices=[])
    name = StringField('Product Name',validators=[DataRequired(),Length(min=4)])
    price = IntegerField('Product Price',validators=[DataRequired()])
    submit = SubmitField('Add Price')

    def validate_category(self,category):   

        try:
            Category.query.filter_by(category_id=uuid.UUID(category.data)).first()
        except:
            raise ValidationError("Invalid category")
    
    def validate_name(self,name):
        try:
            name = SellerPriceList.query.filter_by(product_name = name.data).first()
        except:
            raise ValidationError("Select Category")
        
        if name:
            raise ValidationError("Product name is already exists")
        
class UpdateSellerPriceForm(FlaskForm):
    category = StringField('Category',render_kw={"disabled":'True'})
    name = StringField('Product Name',render_kw={"disabled":'True'})
    price = IntegerField('Product Price',validators=[DataRequired()])
    submit = SubmitField('Update Pricde')

