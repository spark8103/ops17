from flask import render_template, redirect, request, url_for, flash, \
    jsonify
from flask_login import login_required, current_user
from . import project
from .. import db
from ..models import Software, SoftwareSchema

software_schema = SoftwareSchema()
softwares_schema = SoftwareSchema(many=True)


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
        return render_template('project/software.html')
    db.session.delete(software)
    db.session.commit()
    flash('Software: ' + request.form.get('name') + ' is del.')
    return redirect(url_for('.software'))