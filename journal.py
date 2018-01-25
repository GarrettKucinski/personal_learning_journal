from flask import (Flask, g, render_template, redirect, flash, url_for, abort)
from slugify import slugify, slugify_unicode
from flask_login import (LoginManager, login_user,
                         logout_user, login_required, current_user)
from flask_bcrypt import check_password_hash

import datetime

import models
import forms
import re

DEBUG = True
PORT = 8000
HOST = "0.0.0.0"

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Used by Flask to encrypt session cookie.
app.secret_key = "It's a secret to everybody."


@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to database before each request"""

    g.db = models.db
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection"""
    g.db.close()
    return response


@app.route('/')
@app.route('/entries')
@app.route('/archive/<tag>')
def index(tag=''):
    entries = models.Entry.select()

    if tag:
        tag = ' '.join(tag.split('-'))
        entries = entries.where(models.Entry.tags.regexp(r'\b' + tag + r'\b'))

    for entry in entries:
        entry.formatted_date = datetime.datetime.strptime(
            entry.date, "%Y-%m-%d").strftime("%B %d, %Y")

    return render_template('index.html', entries=entries, tag=tag)


@app.route('/entries/<slug>')
def detail(slug):
    entry = models.Entry.get(models.Entry.slug == slug)
    entry.formatted_date = datetime.datetime.strptime(
        entry.date, '%Y-%m-%d').strftime('%B %d, %Y')
    entry.resource_items = filter(None, entry.resources.split('|'))

    if not entry:
        abort(404)

    return render_template('detail.html', entry=entry)


@app.route('/entries/new', methods=("GET", "POST"))
@login_required
def new():
    form = forms.EntryForm()
    if form.validate_on_submit():
        slug = slugify(form.title.data.lower())
        entries = models.Entry.select().where(models.Entry.slug.contains(slug))

        if entries.count() >= 1:
            slug = "{}-{}".format(slug, (entries.count() + 1))

        models.Entry.create(
            title=form.title.data,
            slug=slug,
            date=form.date.data,
            time_spent=form.time_spent.data,
            content=form.content.data,
            resources=form.resources.data,
            tags=form.tags.data
        )
        flash("Entry created successfully!", "success")
        return redirect(url_for('index'))

    return render_template('new.html', form=form)


@app.route('/entries/edit/<slug>', methods=("GET", "POST"))
@login_required
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
@login_required
def delete(slug):
    models.Entry.get(slug=slug).delete_instance()
    flash("Entry has been deleted successfully!", "success")
    return redirect(url_for('index'))


@app.route('/login', methods=("GET", "POST"))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash("That user doesn't exist", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in", "success")
                return redirect(url_for('index'))
            else:
                flash("You're username or password is incorrect", "error")

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out!", "success")

    return redirect(url_for('index'))


if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG, port=PORT, host=HOST)
