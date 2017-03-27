# coding: utf-8
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FloatField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, Software, Project


class AddSoftwareForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    version = StringField('Version')

    def validate_name(self, field):
        if Software.query.filter_by(name=field.data).first():
            raise ValidationError('SoftwareName already in use.')


class EditSoftwareForm(FlaskForm):
    e_id = HiddenField('ID', validators=[Required()])
    e_name = StringField('Name', validators=[Required()])
    e_version = StringField('Version')

    def validate_name(self, field):
        if Software.query.filter_by(name=field.data).first():
            raise ValidationError('SoftwareName already in use.')


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


class EditProjectForm(FlaskForm):
    e_id = HiddenField('ID', validators=[Required()])
    e_name = StringField('Name', validators=[Required()])
    e_department = SelectField('Department', coerce=str)
    e_pm = SelectField('ProjectManager', coerce=int, default=2)
    e_sla = SelectField('SLA', coerce=str)
    e_check_point = StringField('CheckPoint')
    e_domain = StringField('DomainName')
    e_description = TextAreaField('Description')
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(EditProjectForm, self).__init__(*args, **kwargs)
        self.e_pm.choices = [(pm.id, pm.username)
                             for pm in User.query.order_by(User.username).all()]
        self.e_department.choices = [(i, i) for i in current_app.config['DEPARTMENT']]
        self.e_sla.choices = [(i, i) for i in current_app.config['SLA']]

    def validate_name(self, field):
        if Project.query.filter_by(name=field.data).first():
            raise ValidationError('ProjectName already in use.')