from flask import (Flask, g, render_template, redirect, flash, url_for, abort)

import models
import forms

DEBUG = True
PORT = 3000
HOST = "0.0.0.0"

app = Flask(__name__)
app.secret_key = "It's a secret to everyone."


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/detail')
def detail():
    return render_template('detail.html')


@app.route('/new_entry')
def new():
    form = forms.EntryForm()
    return render_template('new.html', form=form)


@app.route('/edit/<entry>')
def edit(entry):
    form = forms.EntryForm()
    return render_template('edit.html', form=form)


if __name__ == "__main__":
    models.initialize()

app.run(debug=DEBUG, port=PORT, host=HOST)
