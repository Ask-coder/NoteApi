from api import Resource, abort, auth, db
from api.models.tag import TagModel
from api.schemas.tag import TagSchema, TagRequestSchema
from api.schemas.tag import tag_schema, tags_schema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc

@doc(description='Api for notes', tags=['Tags'])
class TagResource(MethodResource):
    @doc(summary='Get tag by id', description='Return tag')
    @marshal_with(TagSchema, code=200)
    def get(self, tag_id):
        tag = TagModel.query.get(tag_id)
        if tag is None:
            abort(404, error=f'Tag with {tag_id=} not found')
        return tag, 200


@doc(description='Api for notes', tags=['Tags'])
class TagListResource(MethodResource):
    @doc(summary="Get all tags")
    @marshal_with(TagSchema(many=True), code=200)
    def get(self):
        tags = TagModel.query.all()
        return tags, 200

    @doc(summary="Create new tag")
    @use_kwargs(TagRequestSchema, location='json')
    @marshal_with(TagSchema, code=201)
    def post(self, **kwargs):
        tag = TagModel(**kwargs)
        tag.save()
        if not tag.id:
            abort(400, error=f'Tag {tag.name=} already exist')
        return tag, 201
