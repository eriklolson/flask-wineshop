from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField,  SubmitField, RadioField
from wtforms.validators import DataRequired, Length


# FlaskForm for checkout details
class CheckoutForm(FlaskForm):
    fullname = StringField('Full Name',
                           validators=[DataRequired(), Length(min=2, max=40)])
    card_type = RadioField('card_type')
    card_number = StringField('Credit card number',
                           validators=[DataRequired(), Length(min=12, max=12)])
    expdate = StringField('Exp Date',
                           validators=[DataRequired(), Length(min=4, max=4)])
    cvv = StringField('CVV',
                      validators=[DataRequired(), Length(min=3, max=4)])
    submit = SubmitField('Checkout')


class UpdateCartForm(FlaskForm):
    quantity = IntegerField('Quantity: ', default=1)
