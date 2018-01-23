from flask_wtf import FlaskForm
from wtforms import (StringField, DateField,
                     TextAreaField, FieldList)
from wtforms.validators import DataRequired, Regexp


class EntryForm(FlaskForm):
    title = StringField(u'Title', validators=[DataRequired()])
    date = StringField(
        u'Date',
        validators=[
            DataRequired(),
            Regexp(r'^\d{4}-\d{2}-\d{2}$',
                   message="You must enter a valid date ex. YYYY-MM-DD")
        ])
    time_spent = StringField(u'Time Spent', validators=[DataRequired()])
    content = TextAreaField(u'What I Learned', validators=[DataRequired()])
    resources = TextAreaField(
        u'Resources to Remember',
        validators=[DataRequired()]
    )
