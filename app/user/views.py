from flask import render_template, redirect, request, url_for, flash, \
    current_app, jsonify
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import user
from .. import db
from ..models import User, Role
from ..email import send_email
from .forms import LoginForm, EditProfileForm, ChangePasswordForm, \
    EditUserAdminForm, PasswordResetRequestForm, PasswordResetForm, AddUserAdminForm
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
    page = request.args.get('page', 1, type=int)
    query = User.query
    pagination = query.order_by(User.id.asc()).paginate(
        page, per_page=current_app.config['OPS_USER_PER_PAGE'],
        error_out=False)
    users = pagination.items
    return render_template('user/user_list.html', users=users, pagination=pagination)


@user.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
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


@user.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("user/change_password.html", form=form)


@user.route('/user-edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def user_edit_admin(id):
    user = User.query.get_or_404(id)
    form = EditUserAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.mobile = form.mobile.data
        user.role = Role.query.get(form.role.data)
        user.department = form.department.data
        user.allow_login = form.allow_login.data == str(True)
#        print user.password_hash
        if form.password.data:
            user.password = form.password.data
#        print user.password_hash
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user_edit_admin',id = str(id)))
    form.email.data = user.email
    form.mobile.data = user.mobile
    form.role.data = user.role_id
    form.department.data = user.department
    form.allow_login.data = user.allow_login
    form.password = ''
    return render_template('user/user_edit.html', form=form, user=user.username)


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


@user.route('/del', methods=['POST'])
@login_required
@admin_required
def user_del():
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Non-existent user: ' + username, 'error')
        response = {"success": "false"}
        return jsonify(response)
    db.session.delete(user)
    db.session.commit()
    response = {"success": "true"}
    return jsonify(response)


@user.route('/add', methods=['GET','POST'])
@login_required
@admin_required
def user_add():
    form = AddUserAdminForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    mobile=form.mobile.data,
                    role=Role.query.get(form.role.data),
                    department=form.department.data,
                    allow_login=(form.allow_login.data == str(True)),
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(form.username.data + 'is add.')
        return redirect(url_for('user.user_add'))
    return render_template('user/user_add.html', form=form)