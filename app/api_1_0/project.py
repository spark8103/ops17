from flask import jsonify
from . import api
from ..models import Project, ProjectSchema, Module, ModuleSchema, Environment, EnvironmentSchema, Permission
from .decorators import permission_required

project_schema = ProjectSchema(only=('id', 'name', 'department', 'pm', 'sla', 'check_point', 'description'))
projects_schema = ProjectSchema(many=True, only=('id', 'name', 'department', 'pm', 'sla', 'check_point', 'description'))

module_schema = ModuleSchema(only=('id', 'name', 'project', 'svn', 'parent', 'dev', 'qa', 'ops', 'software',
                                   'description'))
modules_schema = ModuleSchema(many=True, only=('id', 'name', 'project', 'svn', 'parent', 'dev', 'qa', 'ops',
                                               'software', 'description'))

environment_schema = EnvironmentSchema(only=('id', 'module', 'env', 'idc', 'check_point1', 'check_point2',
                                             'check_point3', 'deploy_path', 'server_ip', 'online_since', 'domain'))
environments_schema = EnvironmentSchema(many=True, only=('id', 'module', 'env', 'idc', 'check_point1', 'check_point2',
                                                         'check_point3', 'deploy_path', 'server_ip',
                                                         'online_since', 'domain'))


@api.route('/projects')
@permission_required(Permission.USER)
def get_projects():
    projects = Project.query.all()
    if not projects:
            return jsonify({"message": "Projects could not be found."}), 400
    else:
        # Serialize the queryset
        result = projects_schema.dump(projects)
        return jsonify(result.data)


@api.route('/projects/<int:id>')
@permission_required(Permission.USER)
def get_project(id):
    project = Project.query.get(id)
    if not project:
            return jsonify({"message": "Project could not be found."}), 400
    else:
        # Serialize the queryset
        result = project_schema.dump(project)
        return jsonify(result.data)


@api.route('/modules')
@permission_required(Permission.USER)
def get_modules():
    modules = Module.query.all()
    if not modules:
            return jsonify({"message": "Modules could not be found."}), 400
    else:
        # Serialize the queryset
        result = modules_schema.dump(modules)
        return jsonify(result.data)


@api.route('/modules/<int:id>')
@permission_required(Permission.USER)
def get_module(id):
    module = Module.query.get(id)
    if not module:
            return jsonify({"message": "Module could not be found."}), 400
    else:
        # Serialize the queryset
        result = module_schema.dump(module)
        return jsonify(result.data)


@api.route('/environments')
@permission_required(Permission.USER)
def get_environments():
    environments = Environment.query.all()
    if not environments:
            return jsonify({"message": "Environments could not be found."}), 400
    else:
        # Serialize the queryset
        result = environments_schema.dump(environments)
        return jsonify(result.data)


@api.route('/environments/<int:id>')
@permission_required(Permission.USER)
def get_environment(id):
    environment = Environment.query.get(id)
    if not environment:
            return jsonify({"message": "Environment could not be found."}), 400
    else:
        # Serialize the queryset
        result = environment_schema.dump(environment)
        return jsonify(result.data)