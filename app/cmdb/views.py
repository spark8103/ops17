# coding: utf-8
from flask import render_template, redirect, request, url_for, flash, \
    jsonify
from flask_login import login_required, current_user
from . import cmdb
from .. import db, flash_errors
from ..models import Idc, IdcSchema
from .forms import AddIdcForm, EditIdcForm

idc_schema = IdcSchema()
idcs_schema = IdcSchema(many=True)


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
    id = Idc.query.get_or_404(id)
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