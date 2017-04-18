# coding: utf-8
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FloatField, HiddenField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, Department, Role


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Required(), Length(1, 64),
                                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                   'Usernames must have only letters, '
                                                   'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[Required()])
    password = PasswordField('New password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('New Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class EditProfileForm(FlaskForm):
    email = StringField('New Email', validators=[Required(), Length(1, 64),
                                                 Email()])
    mobile = FloatField("New Mobile", validators=[Required()])
    department = SelectField('Department', coerce=str)
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.department.choices = [(i, i) for i in current_app.config['DEPARTMENT']]


'''
class EditUserAdminForm(FlaskForm):
    email = StringField('New Email', validators=[Required(), Length(1, 64),
                                                 Email()])
    mobile = FloatField("New Mobile", validators=[Required()])
    role = SelectField('New Role', coerce=int)
    department = SelectField('New Department', coerce=str)
    allow_login = SelectField('Allow_login', choices=[("True", "True"),('False','False')])
    password = PasswordField('New Password')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditUserAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.department.choices = [(i, i) for i in current_app.config['DEPARTMENT']]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
'''


class AddUserAdminForm(FlaskForm):
    username = StringField('Username', validators=[
        Required(), Length(3, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                                 Email()])
    mobile = FloatField("Mobile", validators=[Required()])
    department = SelectField('Department', coerce=int)
    role = SelectField('Role', coerce=int, default=2)
    allow_login = SelectField('Allow_login', choices=[("True", "True"),('False','False')], default="False")
    type = SelectField('Type', coerce=str)
    password = PasswordField('Password', validators=[Required()])

    def __init__(self, *args, **kwargs):
        super(AddUserAdminForm, self).__init__(*args, **kwargs)
        self.department.choices = [(department.id, department.name)
                                   for department in Department.query.order_by(Department.name).all()]
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.type.choices = [(i, i) for i in current_app.config['USER_TYPE']]

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class EditUserAdminForm(FlaskForm):
    e_id = HiddenField('ID', validators=[Required()])
    e_username = StringField('Username', validators=[
        Required(), Length(3, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    e_email = StringField('Email', validators=[Required(), Length(1, 64),
                                                 Email()])
    e_mobile = FloatField("Mobile", validators=[Required()])
    e_department = SelectField('Department', coerce=int)
    e_role = SelectField('Role', coerce=int)
    e_allow_login = SelectField('Allow_login', choices=[("True", "True"),('False','False')])
    e_type = SelectField('Type', coerce=str)
    e_password = PasswordField('Password')

    def __init__(self, *args, **kwargs):
        super(EditUserAdminForm, self).__init__(*args, **kwargs)
        self.e_department.choices = [(department.id, department.name)
                                   for department in Department.query.order_by(Department.name).all()]
        self.e_role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.e_type.choices = [(i, i) for i in current_app.config['USER_TYPE']]

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class AddDepartmentForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    parent = SelectField('PerDepartment', coerce=int, default=0)
    description = TextAreaField('Description')

    def __init__(self, *args, **kwargs):
        super(AddDepartmentForm, self).__init__(*args, **kwargs)
        self.parent.choices = [(0, 'None')] + [(parent.id, parent.name)
                            for parent in Department.query.order_by(Department.name).all()]

    def validate_name(self, field):
        if Department.query.filter_by(name=field.data).first():
            raise ValidationError('Department already in use.')


class EditDepartmentForm(FlaskForm):
    e_id = HiddenField('ID', validators=[Required()])
    e_name = StringField('Name', validators=[Required()])
    e_parent = SelectField('PerDepartment', coerce=int)
    e_description = TextAreaField('Description')

    def __init__(self, *args, **kwargs):
        super(EditDepartmentForm, self).__init__(*args, **kwargs)
        self.e_parent.choices = [(0, 'None')] + [(parent.id, parent.name)
                                             for parent in Department.query.order_by(Department.name).all()]

    def validate_name(self, field):
        if Department.query.filter_by(name=field.data).first():
            raise ValidationError('Department already in use.')