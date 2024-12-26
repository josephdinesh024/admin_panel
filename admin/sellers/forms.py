from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField,FileAllowed
from wtforms import StringField, EmailField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from admin.models import Seller


class LoginFrom(FlaskForm):
    #username = StringField('Name',validators=[DataRequired(),Length(min=3)])
    email = EmailField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login')

        
class SellerForm(FlaskForm):
    username = StringField('Seller Name',validators=[DataRequired(),Length(min=3)])
    email = EmailField('Email',validators=[DataRequired(),Email()])
    phone = StringField('Mobile Number',validators=[DataRequired(),Length(min=10,max=10)])
    password = PasswordField('Password',validators=[DataRequired()])
    conform_password = PasswordField('Conform Password',validators=[DataRequired(),EqualTo('password')])
    factory_name = StringField("Company Name",validators=[DataRequired(),Length(min=4,max=25)])
    street = TextAreaField("Street",validators=[DataRequired()])
    city = StringField("City",validators=[DataRequired(),Length(min=4,max=100)])
    state =StringField("State",validators=[DataRequired(),Length(min=4,max=100)])
    postal_code = StringField("Pincode",validators=[DataRequired()])
    country = StringField("Country",validators=[DataRequired()])
    document = MultipleFileField('Document',validators=[DataRequired(),FileAllowed(['jpg','png','jpeg'])])
    description = TextAreaField('Description')
    submit = SubmitField('Register')
    
    def validate_email(self,email):
        seller = Seller.query.filter_by(email_id=email.data).first()
        if seller:
            raise ValidationError("The email already exist. Try another")
    
    def validate_phone(self,phone):
        phone = Seller.query.filter_by(mobile_number=phone.data).first()
        if phone:
            raise ValidationError("The phone number already exist. Try another")
        

    
