from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import Optional, Email, InputRequired, URL, NumberRange

DEMO_IMG = 'https://tinyurl.com/demo-cupcake'


class CupcakeForm(FlaskForm):
    """Form to create cupcake"""
    flavor = StringField("Flavor")
    size = SelectField("Size", choices=[("Small", "Small"), ("Medium", "Medium"), ("Large", "Large")])
    rating = IntegerField("Rating", validators=[NumberRange(min=0, max=10)])
    image = StringField("Image URL")
