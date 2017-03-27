# coding: utf-8
from flask import render_template, redirect, request, url_for, flash, \
    jsonify
from flask_login import login_required, current_user
from flask_restful import Api, Resource, abort
from wtforms import Form, fields, validators
from . import project
from .. import db
from ..models import User, Software, SoftwareSchema, Project, ProjectSchema
from .forms import AddProjectForm

software_schema = SoftwareSchema()
softwares_schema = SoftwareSchema(many=True)
project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)


@project.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()


@project.route('/software')
@login_required
def software():
    return render_template('project/software.html')


@project.route('/software-list')
@login_required
def software_list():
    softwares = Software.query.all()
    if not softwares:
        return jsonify({})
    else:
        # Serialize the queryset
        result = softwares_schema.dump(softwares)
        return jsonify(result.data)


@project.route('/software-add', methods=['POST'])
@login_required
def software_add():
    if request.form.get('name') == '':
        flash('Add software, name is not allow null.')
    elif request.form.get('version') == '':
        flash('Add software, version is not allow null.')
    else:
        software = Software(
            name=request.form.get('name'),
            version=request.form.get('version')
        )
        db.session.add(software)
        db.session.commit()
        flash('software: ' + request.form.get('name') + 'is add.')
    return redirect(url_for('.software'))


@project.route('/software-edit', methods=['POST'])
@login_required
def software_edit():
    id = request.form.get('id')
    software = Software.query.get_or_404(id)
    software.name = request.form.get('name')
    software.version = request.form.get('version')
    db.session.add(software)
    flash('Software: ' + request.form.get('name') + ' is update.')
    return redirect(url_for('.software'))


@project.route('/software-del', methods=['POST'])
@login_required
def software_del():
    id = request.form.get('id')
    software = Software.query.filter_by(id=id).first()
    if software is None:
        flash('Non-existent software: ' + software, 'error')
        return redirect(url_for('.software'))
    db.session.delete(software)
    db.session.commit()
    flash('Software: ' + request.form.get('name') + ' is del.')
    return redirect(url_for('.software'))


@project.route('/')
@login_required
def project_main():
    add_project_form = AddProjectForm()
    return render_template('project/project.html', add_project_form=add_project_form)


@project.route('/list')
@login_required
def project_list():
    projects = Project.query.all()
    if not projects:
        return jsonify({})
    else:
        # Serialize the queryset
        result = projects_schema.dump(projects)
        return jsonify(result.data)


@project.route('/add', methods=['POST'])
@login_required
def project_add():
    form = AddProjectForm(data=request.get_json())
    if form.validate_on_submit():
        project = Project(name=form.name.data,
                          department=form.department.data,
                          pm=User.query.get(form.pm.data),
                          sla=form.sla.data,
                          check_point=form.check_point.data,
                          domain=form.domain.data,
                          description=form.description.data)
        db.session.add(project)
        db.session.commit()
        flash(form.name.data + 'is add.')
    return redirect(url_for('.project_main'))


@project.route('/edit', methods=['POST'])
@login_required
def project_edit():
    id = request.form.get('id')
    project = Project.query.get_or_404(id)
    project.name = request.form.get('name')
    db.session.add(software)
    flash('project: ' + request.form.get('name') + ' is update.')
    return redirect(url_for('.project_main'))


@project.route('/del', methods=['POST'])
@login_required
def project_del():
    id = request.form.get('id')
    project = Project.query.filter_by(id=id).first()
    if project is None:
        flash('Non-existent project: ' + project, 'error')
        return redirect(url_for('.project_main'))
    db.session.delete(project)
    db.session.commit()
    flash('project: ' + request.form.get('name') + ' is del.')
    return redirect(url_for('.project_main'))