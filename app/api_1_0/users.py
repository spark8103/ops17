from flask import jsonify
from . import api
from ..models import User, UserSchema, Department, DepartmentSchema, Permission
from .decorators import permission_required

user_schema = UserSchema(only=('id', 'username', 'department.name', 'email', 'mobile'))

department_schema = DepartmentSchema(only=('id', 'name', 'parent.name', 'description'))
departments_schema = DepartmentSchema(many=True, only=('id', 'name', 'parent.name', 'description'))


@api.route('/users/<int:id>')
@permission_required(Permission.USER)
def get_user(id):
    user = User.query.get(id)
    if not user:
            return jsonify({"message": "User could not be found."}), 400
    else:
        # Serialize the queryset
        result = user_schema.dump(user)
        return jsonify(result.data)


@api.route('/departments')
@permission_required(Permission.USER)
def get_departments():
    departments = Department.query.all()
    if not departments:
            return jsonify({"message": "Departments could not be found."}), 400
    else:
        # Serialize the queryset
        result = departments_schema.dump(departments)
        return jsonify(result.data)


@api.route('/departments/<int:id>')
@permission_required(Permission.USER)
def get_department(id):
    department = Department.query.get(id)
    if not department:
            return jsonify({"message": "Department could not be found."}), 400
    else:
        # Serialize the queryset
        result = department_schema.dump(department)
        return jsonify(result.data)