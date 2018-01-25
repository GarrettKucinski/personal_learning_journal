from flask_wtf import FlaskForm
from wtforms import (StringField, DateField,
                     TextAreaField, FieldList)
from wtforms.validators import DataRequired, Regexp, ValidationError

import datetime


def validate_date_format(form, field):
    try:
        datetime.datetime.strptime(field.data, "%Y-%m-%d")
    except ValueError:
        raise ValidationError(
            "You must enter a valid date in the format yyyy-mm-dd.")


class EntryForm(FlaskForm):
    title = StringField(u"Title", validators=[DataRequired()])
    date = StringField(
        u"Date",
        validators=[
            DataRequired(),
            validate_date_format
        ])
    time_spent = StringField(u"Time Spent", validators=[DataRequired()])
    content = TextAreaField(u"What I've Learned", validators=[DataRequired()])
    resources = TextAreaField(
        u"Resources to Remember",
        render_kw={"placeholder": "Enter comma seperated url, name pairs."
                   "Separate additional pairs with a pipe character."
                   "(ex. http://www.github.com, GitHub|, Resource with no url)"
                   },
        validators=[DataRequired()]
    )
