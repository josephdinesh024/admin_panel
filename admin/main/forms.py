from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from admin.models import Product


class BuyForm(FlaskForm):
    product_id = StringField("id",validators=[DataRequired()])
    quantity = IntegerField("quantity",validators=[DataRequired()])
    purchase_price = IntegerField("price",validators=[DataRequired()])
    submit = SubmitField("Place Order")

    def validate_quantity(self,quantity):
        stock = Product.query.filter_by(product_id=self.product_id.data).first()
        if stock.stock_quantity < quantity.data :
            raise ValidationError("Out of Strock")
        