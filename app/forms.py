from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange

class CharacterSheet(FlaskForm):
    strength = IntegerField('Strength', validators=[NumberRange(min=0)], default=0)
    toughness = IntegerField('Toughness', validators=[NumberRange(min=0)], default=0)
    attacks = IntegerField('Attacks', validators=[NumberRange(min=0)], default=0)
    initiative = IntegerField('Initiative', validators=[NumberRange(min=0)], default=0)
    willpower = IntegerField('Willpower', validators=[NumberRange(min=0)], default=0)
    intelligence = IntegerField('Intelligence', validators=[NumberRange(min=0)], default=0)
    fellowship = IntegerField('Fellowship', validators=[NumberRange(min=0)], default=0)
    armour = IntegerField('Armour', validators=[NumberRange(min=0)], default=0)

class SlimSheet(FlaskForm):
    strength = IntegerField('Strength', validators=[NumberRange(min=0)], default=0)
