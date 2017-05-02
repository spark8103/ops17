from flask import jsonify
from sqlalchemy.exc import IntegrityError
from . import api
from ..models import User, UserSchema, Permission
from .decorators import permission_required

user_schema = UserSchema(only=('id', 'username', 'department.name', 'email', 'mobile'))


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