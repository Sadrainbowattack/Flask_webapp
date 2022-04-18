from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user

from webapp.db import db
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.utils import get_redirect_target

blueprint = Blueprint('user', __name__, url_prefix='/users')

@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(get_redirect_target())
    title = 'Log In'
    login_form = LoginForm()
    return render_template('login.html', page_title=title, form=login_form)

@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Authorization successful')
            return redirect(get_redirect_target())
    flash('Wrong username or password')
    return redirect(url_for('user.login'))

@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Logout successful')
    return redirect(url_for('index.index')) 

@blueprint.route('/registration')
def register():
    if current_user.is_authenticated:
        return redirect(get_redirect_target())
    title = 'Registration'
    registration_form = RegistrationForm()
    return render_template('registration.html', page_title=title, form=registration_form)

@blueprint.route('/progress-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                         email=form.email.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Regestration completed')
        return redirect(get_redirect_target())
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash ('Error in field "{}": - {}'.format(
                    getattr(form, field).label.text, error
                ))
    return redirect(url_for('user.register'))