from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from admin.models import User

class LoginForm(FlaskForm):
    phone_number = IntegerField("Phone Number",validators=[DataRequired(),Length(min=10)])
    otp  = IntegerField("OTP",validators=[DataRequired(),Length(min=6,max=6)])

class ProfileForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired(),Length(min=4,max=25)])
    email = EmailField("Email",validators=[DataRequired(),Email()])
    street = TextAreaField("Street",validators=[DataRequired()])
    city = StringField("City",validators=[DataRequired(),Length(min=4,max=100)])
    state =StringField("State",validators=[DataRequired(),Length(min=4,max=100)])
    postal_code = IntegerField("Pincode",validators=[DataRequired()])
    country = StringField("Country",validators=[DataRequired()])
    submit = SubmitField("Save")

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("The email is taken. Please try another email")