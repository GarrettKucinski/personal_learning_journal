from flask import (Flask, g, render_template, redirect, flash, url_for, abort)
from slugify import slugify, slugify_unicode

import datetime

import models
import forms

DEBUG = True
PORT = 8000
HOST = "0.0.0.0"

app = Flask(__name__)

# Used by Flask to encrypt session cookie.
app.secret_key = "It's a secret to everybody."


@app.route('/')
@app.route('/entries')
def index():
    entries = models.Entry.select()
    for entry in entries:
        entry.formatted_date = datetime.datetime.strptime(
            entry.date, "%Y-%m-%d").strftime("%B %d, %Y")

    return render_template('index.html', entries=entries)


@app.route('/entries/<slug>')
def detail(slug):
    entry = models.Entry.select().where(models.Entry.slug == slug)
    entry[0].formatted_date = datetime.datetime.strptime(
        entry[0].date, '%Y-%m-%d').strftime('%B %d, %Y')
    if entry.count() == 0:
        abort(404)

    return render_template('detail.html', entry=entry[0])


@app.route('/entries/new', methods=("GET", "POST"))
def new():
    form = forms.EntryForm()
    if form.validate_on_submit():
        models.Entry.create(
            title=form.title.data,
            slug=slugify(form.title.data.lower()),
            date=form.date.data,
            time_spent=form.time_spent.data,
            content=form.content.data,
            resources=form.resources.data
        )
        flash("Entry created successfully!", "success")
        return redirect(url_for('index'))

    return render_template('new.html', form=form)


@app.route('/entries/edit/<slug>', methods=("GET", "POST"))
def edit(slug):
    entry = models.Entry.get(slug=slug)
    form = forms.EntryForm(obj=entry)
    if form.validate_on_submit():
        form.populate_obj(entry)
        entry.save()
        flash("You're entry has been updated!")
        return redirect(url_for('detail', slug=slug))

    return render_template('edit.html', form=form)


@app.route('/entries/delete/<slug>')
def delete(slug):
    models.Entry.get(models.Entry.slug == slug).delete_instance()
    flash("Entry has been deleted successfully!", "success")
    return redirect(url_for('index'))


if __name__ == "__main__":
    models.initialize()

app.run(debug=DEBUG, port=PORT, host=HOST)
