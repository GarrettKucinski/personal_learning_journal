from flask import (Flask, g, render_template, redirect, flash, url_for, abort)

import models
import forms

DEBUG = True
PORT = 3000
HOST = "0.0.0.0"

app = Flask(__name__)
app.secret_key = "It's a secret to everybody."


@app.route('/')
def index():
    entries = models.Entry.select()
    return render_template('index.html', entries=entries)


@app.route('/detail/<int:entry_id>')
def detail(entry_id):
    entry = models.Entry.select().where(models.Entry.id == entry_id)
    if entry.count() == 0:
        abort(404)

    return render_template('detail.html', entry=entry[0])


@app.route('/new_entry', methods=("GET", "POST"))
def new():
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.create(
            title=form.title.data,
            date=form.date.data,
            time_spent=form.time_spent.data,
            content=form.content.data,
            resources=form.resources.data
        )
        flash("Entry created successfully!", "success")
        return redirect(url_for('index'))

    return render_template('new.html', form=form)


@app.route('/edit/<entry>')
def edit(entry):
    form = forms.EntryForm()
    return render_template('edit.html', form=form)


if __name__ == "__main__":
    models.initialize()

app.run(debug=DEBUG, port=PORT, host=HOST)
