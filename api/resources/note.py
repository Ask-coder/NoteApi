from api import auth, abort, g, Resource, reqparse, db
from api.models.note import NoteModel
from api.schemas.note import note_schema, notes_schema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from api.schemas.note import NoteSchema
from api.schemas.note import NoteRequestSchema
from api.schemas.tag import TagModel
from webargs import fields


@doc(description='Api for notes', tags=['Notes'])
@doc(security=[{'basicAuth': []}])
class NoteResource(MethodResource):
    @auth.login_required
    @marshal_with(NoteSchema, code=200)
    def get(self, note_id):
        """
        Пользователь может получить ТОЛЬКО свою заметку
        """
        # author = auth.current_user()
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")
        return note_schema.dump(note), 200

    @auth.login_required
    @use_kwargs(NoteRequestSchema, location='json')
    def put(self, **kwargs):
        """
        Пользователь может редактировать ТОЛЬКО свои заметки
        """
        author = auth.current_user()
        note = NoteModel.query.get(kwargs['note_id'])

        if not note:
            abort(404, error=f"note {note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")

        note.text = kwargs["text"]
        note.private = kwargs.get("private") or note.private
        note.save()
        return note_schema.dump(note), 200

    @auth.login_required
    @doc(description='Delete note by id', security=[{"basicAuth": []}])
    @doc(responses={401: {"description": "Not authorization"}})
    @doc(responses={404: {"description": "Not found"}})
    def delete(self, note_id):
        """
        Пользователь может удалять ТОЛЬКО свои заметки
        """
        # author = auth.current_user()
        note = NoteModel.query.get(note_id)

        if note is None:
            return '{"Error": "Note with {note_id=} not found"}', 404

        note.delete()
        return '', 204


@doc(description='Api fot notes', tags=['Notes'])
class NotesListResource(MethodResource):
    @marshal_with(NoteSchema(many=True), code=200)
    def get(self):
        notes = NoteModel.query.all()
        return notes_schema.dump(notes), 200

    @auth.login_required
    @use_kwargs(NoteRequestSchema, location='json')
    def post(self, **kwargs):
        author = auth.current_user()
        print(kwargs)
        note = NoteModel(author_id=author.id, **kwargs)
        note.save()
        return note, 201

@doc(tags=['Notes'])
class NoteSetTagsResource(MethodResource):

    @doc(summary='Set tags to Note')
    @use_kwargs({"tags": fields.List(fields.Int())}, location='json')
    @marshal_with(NoteSchema)
    def put(self, note_id, **kwargs):
        note = NoteModel.query.get(note_id)
        if note is None:
            abort (404, error = f'note_id not found')
        #TODO: Получить все теги по одному запросу
        for tag_id in kwargs["tags"]:
            tag = TagModel.query.get(tag_id)
            note.tags.append(tag)
        db.session.commit()
        return note, 200