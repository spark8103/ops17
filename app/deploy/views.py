# coding: utf-8
from flask import render_template, redirect, request, url_for, flash, \
    jsonify
from flask_login import login_required, current_user
from . import deploy
from .. import db, flash_errors
from ..models import User, Module, Deploy, DeploySchema
from .forms import AddDeployForm

deploy_schema = DeploySchema()
deploys_schema = DeploySchema(many=True)


@deploy.route('/deploy')
@login_required
def deploy_main():
    add_deploy_form = AddDeployForm()
    return render_template('deploy/deploy.html', add_deploy_form=add_deploy_form)


@deploy.route('/deploy-list')
@login_required
def deploy_list():
    if request.args.get('module'):
        deploys = Deploy.query.filter_by(project=Module.query.filter_by(name=request.args.get('module')).first())
    else:
        deploys = Deploy.query.all()
    if not deploys:
        return jsonify({})
    else:
        # Serialize the queryset
        result = deploys_schema.dump(deploys)
        return jsonify(result.data)


@deploy.route('/deploy-add', methods=['POST'])
@login_required
def deploy_add():
    form = AddDeployForm(data=request.get_json())
    if form.validate_on_submit():
        deploy = Deploy(module=Module.query.get(form.module.data),
                        parameter=form.parameter.data,
                        ops=User.query.get(form.ops.data),
                        result=form.result.data)
        db.session.add(deploy)
        db.session.commit()
        flash('deploy: ' + form.module.data + 'is success.')
    else:
        flash_errors(form)
    return redirect(url_for('.deploy_main'))


@deploy.route('/deploy-history')
@login_required
def deploy_history():
    return render_template('deploy/deploy_history.html')