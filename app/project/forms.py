# coding: utf-8
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FloatField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, Project


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Required(), Length(1, 64),
                                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                   'Usernames must have only letters, '
                                                   'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class AddProjectForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    department = SelectField('Department', coerce=str)
    pm = SelectField('ProjectManager', coerce=int, default=2)
    sla = SelectField('SLA', coerce=str)
    check_point = StringField('CheckPoint')
    domain = StringField('DomainName')
    description = TextAreaField('Description')
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(AddProjectForm, self).__init__(*args, **kwargs)
        self.pm.choices = [(pm.id, pm.username)
                             for pm in User.query.order_by(User.username).all()]
        self.department.choices = [(i, i) for i in current_app.config['DEPARTMENT']]
        self.sla.choices = [(i, i) for i in current_app.config['SLA']]

    def validate_name(self, field):
        if Project.query.filter_by(name=field.data).first():
            raise ValidationError('ProjectName already in use.')