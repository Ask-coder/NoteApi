from api import ma
from api.models.tag import TagModel


class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TagModel
        # fields = ('name',)


class TagRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TagModel

    name = ma.Str()


tag_schema = TagSchema()
tags_schema = TagSchema(many=True)