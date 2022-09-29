from api import Resource, abort, reqparse, auth, db
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema
from api.schemas.user import UserSchema, UserRequestSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc


@doc(description='Api for notes.', tags=['Users'])
class UserResource(MethodResource):
    @marshal_with(UserSchema, code=200)
    def get(self, user_id):
        # language=YAML
        """
        Get User by id
        ---
        tags:
            - User
        """
        user = UserModel.query.get(user_id)
        if user is None:
            abort(404, error=f"User with id={user_id} not found")
        return user_schema.dump(user), 200

    @auth.login_required
    @doc(security=[{'basicAuth': []}])
    @use_kwargs(UserRequestSchema, location='json')
    def put(self, **kwargs):
        # language = YAML
        """
        Get User by id
        ---
        tags:
            - Users
        parameters:
            - in: path
              name: user_id
              type: integer
              required: true
              default: 1
        responses:
            200:
                description: A single user item
                schema:
                id: User
                properties:
                id:
                    type: integer
                username:
                    type: string
                is_staff:
                    type: boolean

        """
        user = UserModel.query.get(kwargs['user_id'])
        user.username = kwargs["username"]
        user.password_hash = user.hash_password(kwargs['password'])
        user.save()
        return user_schema.dump(user), 200

    @auth.login_required
    @doc(security=[{'basicAuth': []}])
    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if user is None:
            return {f'User with {user_id=} not found'}, 404

        db.session.delete(user)
        db.session.commit()
        return "", 204


@doc(description='Api for notes', tags=['Users'])
class UsersListResource(MethodResource):
    @marshal_with(UserSchema(many=True), code=200)
    def get(self):
        users = UserModel.query.all()
        return users_schema.dump(users), 200

    @use_kwargs(UserRequestSchema, location='json')
    def post(self, **kwargs):
        user = UserModel(**kwargs)
        user.save()
        if not user.id:
            abort(400, error=f"User with username:{user.username} already exist")
        return user_schema.dump(user), 201
