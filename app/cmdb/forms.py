# coding: utf-8
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TextAreaField, SelectField
from wtforms.validators import InputRequired
from wtforms import ValidationError
from ..models import Software, Idc, Server


class AddSoftwareForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    version = StringField('Version')

    @staticmethod
    def validate_name(self, field):
        if Software.query.filter_by(name=field.data).first():
            raise ValidationError('SoftwareName already in use.')


class EditSoftwareForm(FlaskForm):
    e_id = HiddenField('ID', validators=[InputRequired()])
    e_name = StringField('Name', validators=[InputRequired()])
    e_version = StringField('Version')

    @staticmethod
    def validate_name(self, field):
        if Software.query.filter_by(name=field.data).first():
            raise ValidationError('SoftwareName already in use.')


class AddIdcForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    description = TextAreaField('Description')

    @staticmethod
    def validate_name(self, field):
        if Idc.query.filter_by(name=field.data).first():
            raise ValidationError('IdcName already in use.')


class EditIdcForm(FlaskForm):
    e_id = HiddenField('ID', validators=[InputRequired()])
    e_name = StringField('Name', validators=[InputRequired()])
    e_description = TextAreaField('Description')

    @staticmethod
    def validate_name(self, field):
        if Idc.query.filter_by(name=field.data).first():
            raise ValidationError('IdcName already in use.')


class AddServerForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    idc = SelectField('IDC', coerce=int)
    rack = StringField('Rack')
    private_ip = StringField('Private_ip')
    public_ip = StringField('Public_ip')
    category = StringField('Category')
    category_branch = StringField('Category_Branch')
    env = SelectField('ENV', coerce=str)
    type = SelectField('Type', coerce=str)
    status = SelectField('Status', coerce=str)
    description = TextAreaField('Description')

    def __init__(self, *args, **kwargs):
        super(AddServerForm, self).__init__(*args, **kwargs)
        self.idc.choices = [(0, 'Choose...')] + [(idc.id, idc.name)
                            for idc in Idc.query.order_by(Idc.name).all()]
        self.env.choices = [(i, i) for i in current_app.config['ENVIRONMENT']]
        self.type.choices = [(i, i) for i in current_app.config['SERVER_TYPE']]
        self.status.choices = [(i, i) for i in current_app.config['SERVER_STATUS']]

    @staticmethod
    def validate_name(self, field):
        if Server.query.filter_by(name=field.data).first():
            raise ValidationError('ServerName already in use.')


class EditServerForm(FlaskForm):
    e_id = HiddenField('ID', validators=[InputRequired()])
    e_name = StringField('Name', validators=[InputRequired()])
    e_idc = SelectField('IDC', coerce=int)
    e_rack = StringField('Rack')
    e_private_ip = StringField('Private_ip')
    e_public_ip = StringField('Public_ip')
    e_category = StringField('Category')
    e_category_branch = StringField('Category_Branch')
    e_env = SelectField('ENV', coerce=str)
    e_type = SelectField('Type', coerce=str)
    e_status = SelectField('Status', coerce=str)
    e_description = TextAreaField('Description')

    def __init__(self, *args, **kwargs):
        super(EditServerForm, self).__init__(*args, **kwargs)
        self.e_idc.choices = [(idc.id, idc.name)
                            for idc in Idc.query.order_by(Idc.name).all()]
        self.e_env.choices = [(i, i) for i in current_app.config['ENVIRONMENT']]
        self.e_type.choices = [(i, i) for i in current_app.config['SERVER_TYPE']]
        self.e_status.choices = [(i, i) for i in current_app.config['SERVER_STATUS']]

    @staticmethod
    def validate_name(self, field):
        if Server.query.filter_by(name=field.data).first():
            raise ValidationError('ServerName already in use.')