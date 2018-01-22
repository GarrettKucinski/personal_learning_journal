from flask_wtf import FlaskForm
from wtforms import (StringField, DateTimeField,
                     TextAreaField, FieldList, validators)


class EntryForm(FlaskForm):
    title = StringField(u'Title', [validators.required()])
    date = StringField(u'Date', [validators.required()])
    time_spent = StringField(u'Time Spent', [validators.required()])
    content = TextAreaField(u'What I Learned', [validators.required()])
    resources = TextAreaField(u'Resources to Remember', [
                              validators.required()])
