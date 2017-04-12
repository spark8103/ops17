# coding: utf-8
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TextAreaField
from wtforms.validators import Required
from wtforms import ValidationError
from ..models import Idc


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