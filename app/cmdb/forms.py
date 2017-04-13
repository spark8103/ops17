# coding: utf-8
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TextAreaField, SelectField
from wtforms.validators import Required
from wtforms import ValidationError
from ..models import Idc, Server


class AddIdcForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    description = TextAreaField('Description')

    def validate_name(self, field):
        if Idc.query.filter_by(name=field.data).first():
            raise ValidationError('IdcName already in use.')


class EditIdcForm(FlaskForm):
    e_id = HiddenField('ID', validators=[Required()])
    e_name = StringField('Name', validators=[Required()])
    e_description = TextAreaField('Description')

    def validate_name(self, field):
        if Idc.query.filter_by(name=field.data).first():
            raise ValidationError('IdcName already in use.')


class AddServerForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    idc = SelectField('IDC', coerce=int)
    rack = StringField('Rack')
    private_ip = StringField('Private_ip')
    public_ip = StringField('Public_ip')
    category = StringField('Category')
    env = SelectField('ENV', coerce=str)
    type = SelectField('Type', coerce=str)
    status = SelectField('Status', coerce=str)
    description = TextAreaField('Description')

    def __init__(self, *args, **kwargs):
        super(AddServerForm, self).__init__(*args, **kwargs)
        self.idc.choices = [(idc.id, idc.name)
                            for idc in Idc.query.order_by(Idc.name).all()]
        self.env.choices = [(i, i) for i in current_app.config['ENVIRONMENT']]
        self.type.choices = [("server", "server"),("vserver","vserver")]
        self.status.choices = [(u"在线", u"在线"), (u"备用", u"备用"), (u"维修", u"维修")]

    def validate_name(self, field):
        if Idc.query.filter_by(name=field.data).first():
            raise ValidationError('IdcName already in use.')


class EditServerForm(FlaskForm):
    e_id = HiddenField('ID', validators=[Required()])
    e_name = StringField('Name', validators=[Required()])
    e_idc = SelectField('IDC', coerce=int)
    e_rack = StringField('Rack')
    e_private_ip = StringField('Private_ip')
    e_public_ip = StringField('Public_ip')
    e_category = StringField('Category')
    e_env = SelectField('ENV', coerce=str)
    e_type = SelectField('Type', coerce=str)
    e_status = SelectField('Status', coerce=str)
    e_description = TextAreaField('Description')

    def __init__(self, *args, **kwargs):
        super(EditServerForm, self).__init__(*args, **kwargs)
        self.idc.choices = [(idc.id, idc.name)
                            for idc in Idc.query.order_by(Idc.name).all()]
        self.env.choices = [(i, i) for i in current_app.config['ENVIRONMENT']]
        self.type.choices = [("server", "server"),("vserver","vserver")]
        self.status.choices = [(u"在线", u"在线"), (u"备用", u"备用"), (u"维修", u"维修")]

    def validate_name(self, field):
        if Idc.query.filter_by(name=field.data).first():
            raise ValidationError('IdcName already in use.')