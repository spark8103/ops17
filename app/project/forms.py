# coding: utf-8
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FloatField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, Software, Project, Module


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


class AddModuleForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    project = SelectField('Project', coerce=int, validators=[Required()])
    department = SelectField('Department', coerce=str)
    svn = StringField('SVN')
    parent = SelectField('PerModule', coerce=int, default=0)
    dev = SelectField('DEV', coerce=int)
    qa = SelectField('QA', coerce=int)
    ops = SelectField('OPS', coerce=int)
    software = SelectField('SOFTWARE', coerce=int)
    description = TextAreaField('Description')
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(AddModuleForm, self).__init__(*args, **kwargs)
        self.project.choices = [(project.id, project.name)
                            for project in Project.query.order_by(Project.name).all()]
        self.department.choices = [(i, i) for i in current_app.config['DEPARTMENT']]
        self.parent.choices = [(0, 'None')] + [(parent.id, parent.name)
                            for parent in Module.query.order_by(Module.name).all()]
        self.dev.choices = [(dev.id, dev.username)
                            for dev in User.query.filter_by(department="dev").order_by(User.username).all()]
        self.qa.choices = [(qa.id, qa.username)
                            for qa in User.query.filter_by(department="qa").order_by(User.username).all()]
        self.ops.choices = [(ops.id, ops.username)
                            for ops in User.query.filter_by(department="ops").order_by(User.username).all()]
        self.software.choices = [(software.id, software.version)
                            for software in Software.query.order_by(Software.version).all()]

    def validate_name(self, field):
        if Module.query.filter_by(name=field.data).first():
            raise ValidationError('ModuleName already in use.')


class EditModuleForm(FlaskForm):
    e_id = HiddenField('ID', validators=[Required()])
    e_name = StringField('Name', validators=[Required()])
    e_project = SelectField('Project', coerce=int, validators=[Required()])
    e_department = SelectField('Department', coerce=str)
    e_svn = StringField('SVN')
    e_parent = SelectField('PerModule', coerce=int)
    e_dev = SelectField('DEV', coerce=int)
    e_qa = SelectField('QA', coerce=int)
    e_ops = SelectField('OPS', coerce=int)
    e_software = SelectField('SOFTWARE', coerce=int)
    e_description = TextAreaField('Description')
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(EditModuleForm, self).__init__(*args, **kwargs)
        self.e_project.choices = [(project.id, project.name)
                                for project in Project.query.order_by(Project.name).all()]
        self.e_department.choices = [(i, i) for i in current_app.config['DEPARTMENT']]
        self.e_parent.choices = [(0, 'None')] + [(parent.id, parent.name)
                               for parent in Module.query.order_by(Module.name).all()]
        self.e_dev.choices = [(dev.id, dev.username)
                            for dev in User.query.filter_by(department="dev").order_by(User.username).all()]
        self.e_qa.choices = [(qa.id, qa.username)
                           for qa in User.query.filter_by(department="qa").order_by(User.username).all()]
        self.e_ops.choices = [(ops.id, ops.username)
                            for ops in User.query.filter_by(department="ops").order_by(User.username).all()]
        self.e_software.choices = [(software.id, software.version)
                                 for software in Software.query.order_by(Software.version).all()]

    def validate_name(self, field):
        if Module.query.filter_by(name=field.data).first():
            raise ValidationError('ModuleName already in use.')