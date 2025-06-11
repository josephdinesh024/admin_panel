from collections.abc import Sequence
from typing import Any, Mapping
from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from admin.models import Category
import uuid


class ProductForm(FlaskForm):
    category_id = SelectField('Category',coerce=str,choices=[])
    product_name = SelectField("Product Name",choices=[],validate_choice=False)
    description = TextAreaField("Product Description",validators=[DataRequired()],render_kw={"placeholder":"few words about product & qulaty"})
    price = StringField("Price per Kg",validators=[DataRequired()],render_kw={"readonly":'True'})
    quantity = StringField("Strock Quantity",validators=[DataRequired()],render_kw={"placeholder":"Product quantity you have"}) 
    image = MultipleFileField("Product Image",validators=[DataRequired(),FileAllowed(['jpg','png','jpeg'])])   
    submit = SubmitField("Add Request")

    def validate_category_id(self,category_id):       
        try:
            category = Category.query.filter_by(category_id=uuid.UUID(category_id.data)).first()
        except:
            raise ValidationError("Invalid category. It should not be None")
        
class ProductUpdateForm(FlaskForm):
        
    category_id = StringField("Category",render_kw={"disabled":'True'})
    product_name = StringField("Product Name",render_kw={"disabled":'True'})
    description = TextAreaField("Product Description",validators=[DataRequired()],render_kw={"placeholder":"few words about product & qulaty"})
    price = StringField("Price",render_kw={"disabled":'True'})#validators=[DataRequired(),Length(min=2,max=10)])
    quantity = StringField("Strock Quantity",validators=[DataRequired()]) 
    image = MultipleFileField("Product Image",render_kw={"disabled":'True'})#validators=[FileAllowed(['jpg','png','jpeg'])])   
    submit = SubmitField("Update Request")
