import click
import json
from api.models.note import NoteModel
from api.models.tag import TagModel
from api import db

@click.command
@click.option('--note_id', '-n', multiple=True)
@click.option('--tags_id', '-t', multiple=True)
@click.option('--username', help='Author of note')
@click.option('--is_public')
def add_tags_to_note(note_id, tags_id):
    notes = NoteModel.query.all()
    if note is None:
        print(f'note with {note_id=} not found')
        return

    for id in tags_id:
        tag = TagModel.query.get(id)
        note.tags.append(tag)
    db.session.add(note)
    db.session.commit()

def add_tag(note, tag_id):
    tag = TagModle.query.get(tag_id)
    note.tags.append(tag)

def del_tag(note, tag_id):
    pass

if __name__ == "__main__":
    add_tags_to_note()