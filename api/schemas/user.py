from api import ma
from api.models.user import UserModel
# from api.models.note import NoteModel


#       schema        flask-restful
# object ------>  dict ----------> json


# Сериализация ответа(response)
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        # fields = ('id', 'username', "is_staff")

    id = ma.auto_field()
    username = ma.auto_field()
    is_staff = ma.auto_field()


class UserRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    username = ma.Str()
    password = ma.Str()


user_schema = UserSchema()
users_schema = UserSchema(many=True)
