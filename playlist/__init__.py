import os, json
from jsonschema import validate as validate_json

"""
Not technically a SMPTE standard, just the format we use internally to represent a show playlist
within the TMS. Thought this was the best place for the parse alongside the others for easy discovery :)
"""

class Playlist(object):
    def __init__(self, playlist_contents=None, validate=True):
        self.playlist_contents = playlist_contents

        if self.playlist_contents and validate:
            self.parse(self.playlist_contents)

    def parse(self, playlist_contents=None):
        if playlist_contents:
            self.playlist_contents = playlist_contents

        if type(self.playlist_contents) in [str, unicode]:
            self.playlist_contents = json.loads(self.playlist_contents)

        self.validate()

        # Now we've actually got a validate playlist dictionary lets parse this out into useful structures.
        self.title = self.playlist_contents['title']
        self.duration = self.playlist_contents['duration']

        self.events = []
        for event in self.playlist_contents['events']:
            self.events.append(PlaylistEvent(**event))

    def validate(self, schema_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'schema.json')):
        with open(schema_path) as f:
            schema = f.read()
            schema = json.loads(schema)

            validate_json(self.playlist_contents, schema)

class PlaylistEvent(object):
    def __init__(self, cpl_id, type, text, duration_in_frames, duration_in_seconds, edit_rate):
        self.cpl_id = cpl_id
        self.type = type
        self.text = text
        self.duration_in_frames = duration_in_frames
        self.duration_in_seconds = duration_in_seconds
        self.edit_rate = edit_rate