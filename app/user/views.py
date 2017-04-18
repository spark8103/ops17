# coding: utf-8
from flask import render_template, redirect, request, url_for, flash, \
    current_app, jsonify
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import user
from .. import db, flash_errors
from ..models import User, UserSchema, Department, DepartmentSchema, Role
from ..email import send_email
from .forms import LoginForm, EditProfileForm, ChangePasswordForm, \
    PasswordResetRequestForm, PasswordResetForm, AddUserAdminForm, EditUserAdminForm, \
    AddDepartmentForm, EditDepartmentForm
from ..decorators import admin_required, permission_required

user_schema = UserSchema()
users_schema = UserSchema(many=True)
department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)


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

''' old code
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
        if form.password.data:
            user.password = form.password.data
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
'''

@user.route('/useradmin')
@login_required
@admin_required
def useradmin():
    add_useradmin_form = AddUserAdminForm()
    edit_useradmin_form = EditUserAdminForm()
    return render_template('user/useradmin.html', add_useradmin_form=add_useradmin_form,
                           edit_useradmin_form=edit_useradmin_form)


@user.route('/useradmin-list')
@login_required
@admin_required
def useradmin_list():
    users = User.query.all()
    if not users:
        return jsonify({})
    else:
        # Serialize the queryset
        result = users_schema.dump(users)
        return jsonify(result.data)


@user.route('/useradmin-add', methods=['POST'])
@login_required
@admin_required
def useradmin_add():
    form = AddUserAdminForm(data=request.get_json())
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            mobile=form.mobile.data,
            department=Department.query.get(form.department.data),
            role=Role.query.get(form.role.data),
            allow_login=(form.allow_login.data == str(True)),
            type=form.type.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('user: ' + request.form.get('username') + ' is add.')
    else:
        flash_errors(form)
    return redirect(url_for('.useradmin'))


@user.route('/useradmin-edit', methods=['POST'])
@login_required
@admin_required
def useradmin_edit():
    id = request.form.get('e_id')
    user = User.query.get_or_404(id)
    form = EditUserAdminForm(id=id)
    if form.validate_on_submit():
        user.username = form.e_username.data
        user.email = form.e_email.data
        user.mobile = form.e_mobile.data
        user.department = Department.query.get(form.e_department.data)
        user.role = Role.query.get(form.e_role.data)
        user.allow_login = (form.e_allow_login.data == str(True))
        user.type = form.e_type.data
        if form.e_password.data:
            user.password = form.e_password.data
        db.session.add(user)
        flash('user: ' + request.form.get('e_username') + ' is update.')
    else:
        flash_errors(form)
    return redirect(url_for('.useradmin'))


@user.route('/useradmin-del', methods=['POST'])
@login_required
@admin_required
def useradmin_del():
    id = request.form.get('id')
    user = User.query.filter_by(id=id).first()
    if user is None:
        flash('Non-existent user: ' + request.form.get('username'), 'error')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('user: ' + request.form.get('username') + ' is del.')
    return redirect(url_for('.useradmin'))


@user.route('/department')
@login_required
@admin_required
def department():
    add_department_form = AddDepartmentForm()
    edit_department_form = EditDepartmentForm()
    return render_template('user/department.html', add_department_form=add_department_form,
                           edit_department_form=edit_department_form)


@user.route('/department-list')
@login_required
@admin_required
def department_list():
    departments = Department.query.all()
    if not departments:
        return jsonify({})
    else:
        # Serialize the queryset
        result = departments_schema.dump(departments)
        return jsonify(result.data)


@user.route('/department-add', methods=['POST'])
@login_required
@admin_required
def department_add():
    form = AddDepartmentForm(data=request.get_json())
    if form.validate_on_submit():
        department = Department(
            name=form.name.data,
            parent=Department.query.get(form.parent.data),
            description=form.description.data
        )
        db.session.add(department)
        db.session.commit()
        flash('department: ' + request.form.get('name') + ' is add.')
    else:
        flash_errors(form)
    return redirect(url_for('.department'))


@user.route('/department-edit', methods=['POST'])
@login_required
@admin_required
def department_edit():
    id = request.form.get('e_id')
    department = Department.query.get_or_404(id)
    form = EditDepartmentForm(id=id)
    if form.validate_on_submit():
        department.name = form.e_name.data
        department.parent = Department.query.get(form.e_parent.data)
        department.description = form.e_description.data
        db.session.add(department)
        flash('department: ' + request.form.get('e_name') + ' is update.')
    else:
        flash_errors(form)
    return redirect(url_for('.department'))


@user.route('/department-del', methods=['POST'])
@login_required
@admin_required
def department_del():
    id = request.form.get('id')
    department = Department.query.filter_by(id=id).first()
    if department is None:
        flash('Non-existent department: ' + request.form.get('name'), 'error')
    else:
        db.session.delete(department)
        db.session.commit()
        flash('department: ' + request.form.get('name') + ' is del.')
    return redirect(url_for('.department'))