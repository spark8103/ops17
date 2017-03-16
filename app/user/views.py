from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import user
from .. import db
from ..models import User, Role
from ..email import send_email
from .forms import LoginForm, EditProfileForm, \
    EditProfileAdminForm, PasswordResetRequestForm, PasswordResetForm
from ..decorators import admin_required, permission_required


@user.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = User.query.filter_by(username=form.username.data).first()
        if username is not None and username.allow_login and username.verify_password(form.password.data):
            login_user(username, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('user/login.html', form=form)


@user.route('/user-list')
@login_required
def user_list():
    user_list = User.query.all()
    print user_list[0].role
    return render_template('user/user.html', user_list=user_list)


@user.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    print form.data
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.mobile = form.mobile.data
        current_user.department = form.department.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('user.edit_profile'))
    form.email.data = current_user.email
    form.mobile.data = current_user.mobile
    form.department.data = current_user.department
    form.about_me.data = current_user.about_me
    return render_template('user/edit_profile.html', form=form)


@user.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@user.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'user/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('user.login'))
    return render_template('user/reset_password.html', form=form)


@user.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('user.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('user/reset_password.html', form=form)