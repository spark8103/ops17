# coding: utf-8
from flask import render_template, redirect, request, url_for, flash, \
    jsonify, current_app
from flask_login import login_required, current_user
from . import cmdb
from .. import db, flash_errors
from ..models import Software, SoftwareSchema, Idc, IdcSchema, Server, ServerSchema
from .forms import AddSoftwareForm, EditSoftwareForm, AddIdcForm, EditIdcForm, AddServerForm, EditServerForm
from werkzeug.utils import secure_filename
import os, csv
from HTMLParser import HTMLParser

software_schema = SoftwareSchema()
softwares_schema = SoftwareSchema(many=True)
idc_schema = IdcSchema()
idcs_schema = IdcSchema(many=True)
server_schema = ServerSchema()
servers_schema = ServerSchema(many=True)

ALLOWED_EXTENSIONS = set(['csv'])


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@cmdb.route('/software')
@login_required
def software():
    add_software_form = AddSoftwareForm()
    edit_software_form = EditSoftwareForm()
    return render_template('cmdb/software.html', add_software_form=add_software_form,
                           edit_software_form=edit_software_form)


@cmdb.route('/software-list')
@login_required
def software_list():
    softwares = Software.query.all()
    if not softwares:
        return jsonify({})
    else:
        # Serialize the queryset
        result = softwares_schema.dump(softwares)
        return jsonify(result.data)


@cmdb.route('/software-add', methods=['POST'])
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


@cmdb.route('/software-edit', methods=['POST'])
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


@cmdb.route('/software-del', methods=['POST'])
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


@cmdb.route('/idc')
@login_required
def idc():
    add_idc_form = AddIdcForm()
    edit_idc_form = EditIdcForm()
    return render_template('cmdb/idc.html', add_idc_form=add_idc_form,
                           edit_idc_form=edit_idc_form)


@cmdb.route('/idc-list')
@login_required
def idc_list():
    idcs = Idc.query.all()
    if not idcs:
        return jsonify({})
    else:
        # Serialize the queryset
        result = idcs_schema.dump(idcs)
        return jsonify(result.data)


@cmdb.route('/idc-add', methods=['POST'])
@login_required
def idc_add():
    form = AddIdcForm(data=request.get_json())
    if form.validate_on_submit():
        idc = Idc(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(idc)
        db.session.commit()
        flash('idc: ' + request.form.get('name') + ' is add.')
    else:
        flash_errors(form)
    return redirect(url_for('.idc'))


@cmdb.route('/idc-edit', methods=['POST'])
@login_required
def idc_edit():
    id = request.form.get('e_id')
    idc = Idc.query.get_or_404(id)
    form = EditIdcForm(id=id)
    if form.validate_on_submit():
        idc.name = form.e_name.data
        idc.description = form.e_description.data
        db.session.add(idc)
        flash('idc: ' + request.form.get('e_name') + ' is update.')
    else:
        flash_errors(form)
    return redirect(url_for('.idc'))


@cmdb.route('/idc-del', methods=['POST'])
@login_required
def idc_del():
    id = request.form.get('id')
    idc = Idc.query.filter_by(id=id).first()
    if idc is None:
        flash('Non-existent idc: ' + request.form.get('name'), 'error')
    else:
        db.session.delete(idc)
        db.session.commit()
        flash('idc: ' + request.form.get('name') + ' is del.')
    return redirect(url_for('.idc'))


@cmdb.route('/server')
@login_required
def server():
    add_server_form = AddServerForm()
    edit_server_form = EditServerForm()
    return render_template('cmdb/server.html', add_server_form=add_server_form,
                           edit_server_form=edit_server_form)


@cmdb.route('/server-list')
@login_required
def server_list():
    if request.args.get('category_branch'):
        servers = Server.query.filter_by(category_branch=request.args.get('category_branch')).all()
    else:
        servers = Server.query.all()
    if not servers:
        return jsonify({})
    else:
        # Serialize the queryset
        result = servers_schema.dump(servers)
        return jsonify(result.data)


@cmdb.route('/server-add', methods=['POST'])
@login_required
def server_add():
    form = AddServerForm(data=request.get_json())
    if form.validate_on_submit():
        server = Server(
            name=form.name.data,
            idc=Idc.query.get(form.idc.data),
            rack=form.rack.data,
            private_ip=form.private_ip.data,
            public_ip=form.private_ip.data,
            category=form.category.data,
            category_branch=form.category_branch.data,
            env=form.env.data,
            type=form.type.data,
            status=form.status.data,
            description=form.description.data,
        )
        db.session.add(server)
        db.session.commit()
        flash('server: ' + request.form.get('name') + ' is add.')
    else:
        flash_errors(form)
    return redirect(url_for('.server'))


@cmdb.route('/server-edit', methods=['POST'])
@login_required
def server_edit():
    id = request.form.get('e_id')
    server = Server.query.get_or_404(id)
    form = EditServerForm(id=id)
    if form.validate_on_submit():
        server.name = form.e_name.data
        server.idc = Idc.query.get(form.e_idc.data)
        server.rack = form.e_rack.data
        server.private_ip = form.e_private_ip.data
        server.public_ip = form.e_public_ip.data
        server.category = form.e_category.data
        server.category_branch = form.e_category_branch.data
        server.env = form.e_env.data
        server.type = form.e_type.data
        server.status = form.e_status.data
        server.description = form.e_description.data
        db.session.add(server)
        flash('server: ' + request.form.get('e_name') + ' is update.')
    else:
        flash_errors(form)
    return redirect(url_for('.server'))


@cmdb.route('/server-del', methods=['POST'])
@login_required
def server_del():
    id = request.form.get('id')
    server = Server.query.filter_by(id=id).first()
    if idc is None:
        flash('Non-existent server: ' + request.form.get('name'), 'error')
    else:
        db.session.delete(server)
        db.session.commit()
        flash('server: ' + request.form.get('name') + ' is del.')
    return redirect(url_for('.server'))


@cmdb.route('/server-import', methods=['GET', 'POST'])
@login_required
def server_import():
    if request.method == 'POST':
        upload_file = request.files['file']
        if upload_file and allowed_file(upload_file.filename):
            filename = secure_filename(upload_file.filename)
            upload_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), 'rb') as csv_file:
                reader = csv.DictReader(csv_file)
                column = [row for row in reader]
                for line in column:
                    server = Server.query.filter_by(name=strip_tags(line["name"])).first()
                    if server is None:
                        server = Server(name=strip_tags(line["name"]))
                    server.idc = Idc.query.filter_by(name=strip_tags(line["idc"])).first()
                    server.rack = strip_tags(line["rack"])
                    server.private_ip = strip_tags(line["private_ip"])
                    server.public_ip = strip_tags(line["public_ip"])
                    server.category = strip_tags(line["category"])
                    server.category_branch = strip_tags(line["category_branch"])
                    server.env = strip_tags(line["env"])
                    server.type = strip_tags(line["type"])
                    server.status = strip_tags(line["status"])
                    server.description = strip_tags(line["description"])
                    db.session.add(server)
                    db.session.commit()

            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            flash('upload file: ' + filename + ' is ok.')
            data = column
        else:
            flash("upload file:" + upload_file.filename + " is error.")
            data = ''
    else:
        data = ''
    return render_template('cmdb/server_import.html', data=data)


@cmdb.route('/category_branch-list')
@login_required
def category_branch_list():
    category_branch = Server.query.with_entities(Server.category_branch).group_by(Server.category_branch).all()
    if not category_branch:
        return jsonify({})
    else:
        # Serialize the queryset
        result = [i[0] for i in category_branch]
        return jsonify(result)