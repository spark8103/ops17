# coding: utf-8
from flask import render_template, redirect, request, url_for, flash, \
    jsonify
from flask_login import login_required, current_user
from . import project
from .. import db, flash_errors
from ..models import User, Software, SoftwareSchema, Project, ProjectSchema, Module, ModuleSchema
from .forms import AddProjectForm, EditProjectForm, AddSoftwareForm, EditSoftwareForm, AddModuleForm, EditModuleForm

software_schema = SoftwareSchema()
softwares_schema = SoftwareSchema(many=True)
project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)
module_schema = ModuleSchema()
modules_schema = ModuleSchema(many=True)


@project.route('/software')
@login_required
def software():
    add_software_form = AddSoftwareForm()
    edit_software_form = EditSoftwareForm()
    return render_template('project/software.html', add_software_form=add_software_form,
                           edit_software_form=edit_software_form)


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
    form = AddSoftwareForm(data=request.get_json())
    if form.validate_on_submit():
        software = Software(
            name=form.name.data,
            version=form.version.data
        )
        db.session.add(software)
        db.session.commit()
        flash('software: ' + request.form.get('name') + ' is add.')
    else:
        flash_errors(form)
    return redirect(url_for('.software'))


@project.route('/software-edit', methods=['POST'])
@login_required
def software_edit():
    id = request.form.get('e_id')
    software = Software.query.get_or_404(id)
    form = EditSoftwareForm(id=id)
    if form.validate_on_submit():
        software.name = form.e_name.data
        software.version = form.e_version.data
        db.session.add(software)
        flash('Software: ' + request.form.get('e_name') + ' is update.')
    else:
        flash_errors(form)
    return redirect(url_for('.software'))


@project.route('/software-del', methods=['POST'])
@login_required
def software_del():
    id = request.form.get('id')
    software = Software.query.filter_by(id=id).first()
    if software is None:
        flash('Non-existent software: ' + request.form.get('name'), 'error')
    else:
        db.session.delete(software)
        db.session.commit()
        flash('Software: ' + request.form.get('name') + ' is del.')
    return redirect(url_for('.software'))


@project.route('/')
@login_required
def project_main():
    add_project_form = AddProjectForm()
    edit_project_form = EditProjectForm()
    return render_template('project/project.html', add_project_form=add_project_form,
                           edit_project_form=edit_project_form)


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
        flash('project: ' + form.name.data + ' is add.')
    else:
        flash_errors(form)
    return redirect(url_for('.project_main'))


@project.route('/edit', methods=['POST'])
@login_required
def project_edit():
    id = request.form.get('e_id')
    project = Project.query.get_or_404(id)
    form = EditProjectForm(id=id)
    if form.validate_on_submit():
        project.name = form.e_name.data
        project.department = form.e_department.data
        project.pm = User.query.get(form.e_pm.data)
        project.sla = form.e_sla.data
        project.check_point = form.e_check_point.data
        project.domain = form.e_domain.data
        project.description = form.e_description.data
        db.session.add(project)
        flash('project: ' + request.form.get('e_name') + ' is update.')
    else:
        flash_errors(form)
    return redirect(url_for('.project_main'))


@project.route('/del', methods=['POST'])
@login_required
def project_del():
    id = request.form.get('id')
    project = Project.query.filter_by(id=id).first()
    if project is None:
        flash('Non-existent project: ' + request.form.get('name'), 'error')
    else:
        db.session.delete(project)
        db.session.commit()
        flash('project: ' + request.form.get('name') + ' is del.')
    return redirect(url_for('.project_main'))


@project.route('/module')
@login_required
def module_main():
    add_module_form = AddModuleForm()
    edit_module_form = EditModuleForm()
    return render_template('project/module.html', add_module_form=add_module_form,
                           edit_module_form=edit_module_form)


@project.route('/module-list')
@login_required
def module_list():
    modules = Module.query.all()
    if not modules:
        return jsonify({})
    else:
        # Serialize the queryset
        result = modules_schema.dump(modules)
        return jsonify(result.data)


@project.route('/module-add', methods=['POST'])
@login_required
def module_add():
    form = AddModuleForm(data=request.get_json())
    if form.validate_on_submit():
        module = Module(name=form.name.data,
                        project=Project.query.get(form.project.data),
                        department=form.department.data,
                        svn=form.svn.data,
                        parent=Module.query.get(form.parent.data),
                        dev=User.query.get(form.dev.data),
                        qa=User.query.get(form.qa.data),
                        ops=User.query.get(form.ops.data),
                        software=Software.query.get(form.software.data),
                        description=form.description.data)
        db.session.add(module)
        db.session.commit()
        flash('module: ' + form.name.data + 'is add.')
    else:
        flash_errors(form)
    return redirect(url_for('.module_main'))


@project.route('/module-edit', methods=['POST'])
@login_required
def module_edit():
    id = request.form.get('e_id')
    module = Module.query.get_or_404(id)
    form = EditModuleForm(id=id)
    if form.validate_on_submit():
        module.name = form.e_name.data
        module.project = Project.query.get(form.e_project.data)
        module.department = form.e_department.data
        module.svn = form.e_svn.data
        module.parent = Module.query.get(form.e_parent.data)
        module.dev = User.query.get(form.e_dev.data)
        module.qa = User.query.get(form.e_qa.data)
        module.ops = User.query.get(form.e_ops.data)
        module.software = Software.query.get(form.e_software.data)
        module.description = form.e_description.data
        db.session.add(module)
        flash('module: ' + form.e_name.data + ' is update.')
    else:
        flash_errors(form)
    return redirect(url_for('.module_main'))


@project.route('/module-del', methods=['POST'])
@login_required
def module_del():
    id = request.form.get('id')
    module = Module.query.filter_by(id=id).first()
    if module is None:
        flash('Non-existent module: ' + request.form.get('name'), 'error')
    else:
        db.session.delete(module)
        db.session.commit()
        flash('module: ' + request.form.get('name') + ' is del.')
    return redirect(url_for('.module_main'))


@project.route('/environment')
@login_required
def environment_main():
    add_module_form = AddModuleForm()
    edit_module_form = EditModuleForm()
    return render_template('project/module.html', add_module_form=add_module_form,
                           edit_module_form=edit_module_form)


@project.route('/environment-list')
@login_required
def environment_list():
    modules = Module.query.all()
    if not modules:
        return jsonify({})
    else:
        # Serialize the queryset
        result = modules.dump(modules)
        return jsonify(result.data)


@project.route('/environment-add', methods=['POST'])
@login_required
def environment_add():
    form = AddModuleForm(data=request.get_json())
    print form.data
    if form.validate_on_submit():
        module = Module(name=form.name.data,
                        project=Project.query.get(form.project.data),
                        department=form.department.data,
                        svn=form.svn.data,
                        parent=Module.query.get(form.parent.data),
                        dev=User.query.get(form.dev.data),
                        qa=User.query.get(form.qa.data),
                        ops=User.query.get(form.ops.data),
                        software=Software.query.get(form.software.data),
                        description=form.description.data)
        db.session.add(module)
        db.session.commit()
        flash('environment: ' + form.name.data + 'is add.')
    else:
        flash_errors(form)
    return redirect(url_for('.module_main'))


@project.route('/environment-edit', methods=['POST'])
@login_required
def environment_edit():
    id = request.form.get('e_id')
    module = Module.query.get_or_404(id)
    module.name = request.form.get('e_name')
    module.project = Project.query.get(request.form.get('e_project')),
    module.department = request.form.get('e_department')
    module.svn = request.form.get('e_svn')
    module.parent = Project.query.get(request.form.get('e_parent'))
    module.dev = User.query.get(request.form.get('e_dev'))
    module.qa = User.query.get(request.form.get('e_qa'))
    module.ops = User.query.get(request.form.get('e_ops'))
    module.software = Software.query.get(request.form.get('e_software'))
    module.description = request.form.get('e_description')
    db.session.add(module)
    flash('environment: ' + request.form.get('e_name') + ' is update.')
    return redirect(url_for('.module_main'))


@project.route('/environment-del', methods=['POST'])
@login_required
def environment_del():
    id = request.form.get('id')
    module = Module.query.filter_by(id=id).first()
    if module is None:
        flash('Non-existent module: ' + request.form.get('name'), 'error')
        return redirect(url_for('.module_main'))
    db.session.delete(module)
    db.session.commit()
    flash('environment: ' + request.form.get('name') + ' is del.')
    return redirect(url_for('.module_main'))