from flask_wtf import Form
from wtforms import (StringField, DateTimeField,
                     TextAreaField, FieldList, validators)


class EntryForm(Form):
    title = StringField(u'Title', [validators.required()])
    date = DateTimeField(u'Date', [validators.required()])
    time_spent = StringField(u'Time Spent', [validators.required()])
    content = TextAreaField(u'What I Learned', [validators.required()])
    resources = TextAreaField(u'Resources to Remember', [
                              validators.required()])
