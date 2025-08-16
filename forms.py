from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length

class DataEntryForm(FlaskForm):
    """Form for data entry"""
    
    name = StringField('Name', validators=[
        DataRequired(message="Name is required"),
        Length(min=2, max=255, message="Name must be between 2 and 255 characters")
    ])
    
    email = StringField('Email', validators=[
        Optional(),
        Email(message="Please enter a valid email address")
    ])
    
    phone = StringField('Phone', validators=[
        Optional(),
        Length(max=50, message="Phone number must be less than 50 characters")
    ])
    
    category = SelectField('Category', choices=[
        ('', 'Select a category'),
        ('personal', 'Personal'),
        ('business', 'Business'),
        ('education', 'Education'),
        ('health', 'Health'),
        ('technology', 'Technology'),
        ('other', 'Other')
    ], validators=[Optional()])
    
    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=1000, message="Description must be less than 1000 characters")
    ])
    
    submit = SubmitField('Save Entry')