from flask import jsonify
from . import api
from ..models import Software, SoftwareSchema, Idc, IdcSchema, Server, ServerSchema, Permission
from .decorators import permission_required

software_schema = SoftwareSchema(only=('id', 'name', 'version'))
softwares_schema = SoftwareSchema(many=True, only=('id', 'name', 'version'))

idc_schema = IdcSchema(only=('id', 'name', 'description'))
idcs_schema = IdcSchema(many=True, only=('id', 'name', 'description'))

server_schema = ServerSchema(only=('id', 'category_branch', 'name', 'idc', 'rack', 'private_ip', 'public_ip', 'category', 'env',
                                   'type', 'status', 'description'))
servers_schema = ServerSchema(many=True, only=('id', 'category_branch', 'name', 'idc', 'rack', 'private_ip', 'public_ip',
                                               'category', 'env', 'type', 'status', 'description'))


@api.route('/softwares')
@permission_required(Permission.USER)
def get_softwares():
    softwares = Software.query.all()
    if not softwares:
            return jsonify({"message": "Softwares could not be found."}), 400
    else:
        # Serialize the queryset
        result = softwares_schema.dump(softwares)
        return jsonify(result.data)


@api.route('/softwares/<int:id>')
@permission_required(Permission.USER)
def get_software(id):
    software = Software.query.get(id)
    if not software:
            return jsonify({"message": "Software could not be found."}), 400
    else:
        # Serialize the queryset
        result = software_schema.dump(software)
        return jsonify(result.data)


@api.route('/idcs')
@permission_required(Permission.USER)
def get_idcs():
    idcs = Idc.query.all()
    if not idcs:
            return jsonify({"message": "Idcs could not be found."}), 400
    else:
        # Serialize the queryset
        result = idcs_schema.dump(idcs)
        return jsonify(result.data)


@api.route('/idcs/<int:id>')
@permission_required(Permission.USER)
def get_idc(id):
    idc = Idc.query.get(id)
    if not idc:
            return jsonify({"message": "Idc could not be found."}), 400
    else:
        # Serialize the queryset
        result = idc_schema.dump(idc)
        return jsonify(result.data)


@api.route('/servers')
@permission_required(Permission.USER)
def get_servers():
    servers = Server.query.all()
    if not servers:
            return jsonify({"message": "Servers could not be found."}), 400
    else:
        # Serialize the queryset
        result = servers_schema.dump(servers)
        return jsonify(result.data)


@api.route('/servers/<int:id>')
@permission_required(Permission.USER)
def get_server(id):
    server = Server.query.get(id)
    if not server:
            return jsonify({"message": "Server could not be found."}), 400
    else:
        # Serialize the queryset
        result = server_schema.dump(server)
        return jsonify(result.data)