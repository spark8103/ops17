# coding: utf-8
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TextAreaField, SelectField
from wtforms.validators import InputRequired
from wtforms import ValidationError
from ..models import User, Project, Module, Deploy


class AddDeployForm(FlaskForm):
    project = SelectField('Project', coerce=int)
    module = SelectField('Module', coerce=int, validators=[InputRequired()])
    parameter = StringField('Parameter', validators=[InputRequired()])
    ops = SelectField('Ops', coerce=int, validators=[InputRequired()])
    result = TextAreaField('Parameter', validators=[InputRequired()])

    def __init__(self, *args, **kwargs):
        super(AddDeployForm, self).__init__(*args, **kwargs)
        self.project.choices = [(0, 'Choose...')] + [(project.id, project.name)
                               for project in Project.query.order_by(Project.name).all()]
        self.module.choices = [(0, 'Choose...')] + [(module.id, module.name)
                               for module in Module.query.order_by(Module.name).all()]
        self.ops.choices = [(0, 'None')] + [(ops.id, ops.username)
                                            for ops in User.query.filter_by(type="ops").order_by(User.username).all()]

    @staticmethod
    def validate_name(self, field):
        if Deploy.query.filter_by(name=field.data).first():
            raise ValidationError('DeployName already in use.')