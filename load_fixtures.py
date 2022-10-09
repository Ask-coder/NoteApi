import click

from api import db
import json
#from api.schemas.user import UserRequestSchema
from api.models.note import NoteModel
from api.models.user import UserModel
from api.models.tag import TagModel
from config import Config


@click.command
# @click.argument('file_name') # python load_fixtures.py 'notes.json'
@click.option('--file_name', help='fixture file name') # python load_fixtures.py --file_name 'notes.json'
def load_data(file_name):
    with open(Config.PATH_TO_FIXTURES / file_name, "r", encoding="UTF-8") as f:
        file_data = json.load(f)
        model_name = file_data["model"]
        tmp = ''
        if model_name == "UserModel":
            model = UserModel
            tmp = 'user'

        elif model_name == "NoteModel":
            model = NoteModel
            tmp = 'note'

        elif model_name == "TagModel":
            model = TagModel
            tmp = 'tag'

        for obj_data in file_data["data"]:
            obj = model(**obj_data)
            db.session.add(obj)
        db.session.commit()
    print(f"{len(file_data['data'])} {tmp}(s) created")

#
# path_to_fixture = "fixtures/users.json"
# load_data(path_to_fixture)


if __name__ == "__main__":
    load_data()