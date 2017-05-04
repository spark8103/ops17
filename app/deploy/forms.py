# coding: utf-8
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TextAreaField, SelectField
from wtforms.validators import Required
from wtforms import ValidationError
from ..models import User, Module, Deploy


class AddDeployForm(FlaskForm):
    module = SelectField('Module', coerce=int, validators=[Required()])
    parameter = StringField('Parameter', validators=[Required()])
    ops = SelectField('Ops', coerce=int, validators=[Required()])
    result = TextAreaField('Parameter', validators=[Required()])

    def __init__(self, *args, **kwargs):
        super(AddDeployForm, self).__init__(*args, **kwargs)
        self.module.choices = [(module.id, module.name)
                               for module in Module.query.order_by(Module.name).all()]
        self.ops.choices = [(0, 'None')] + [(ops.id, ops.username)
                                            for ops in User.query.filter_by(type="ops").order_by(User.username).all()]

    @staticmethod
    def validate_name(self, field):
        if Deploy.query.filter_by(name=field.data).first():
            raise ValidationError('DeployName already in use.')