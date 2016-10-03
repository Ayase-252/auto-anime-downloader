"""Anime model."""

from datetime import date

import database_new as database
from .datamodel import DataModel


class Anime(DataModel):
    """Anime model.

    Attributes:
        name: Name of anime(Required).
        start_day: Day when anime premires(Required).
        total_episode: Total episodes.
        offset: Episodes offset.
        downloaded_episode: Episode which have been downloaded.
        translation_team: Translation team which you are favor of

        keyword: Keyword to search. Use directory so scraper can be set
            individually.

        folder: Subfolder name of download destination, if you enable auto
            download episode function.
    """

    _primary_key = 'name'

    def __init__(self, name, start_day=date.today(), total_ep=99,
                 offset=0, downloaded_episode=[], translation_team=[],
                 keyword={}, folder=''):
        """Initial an anime instance.

        Args refers to class docstring.
        """
        self.name = name
        self.start_day = start_day
        self.total_ep = total_ep
        self.offset = offset
        self.downloaded_episode = downloaded_episode
        self.translation_team = translation_team
        self.keyword = keyword
        self.folder = folder

    def to_dict(self):
        """Return dictionary resentation of instance."""
        pass

    def save(self):
        """Save instance in database.

        Create an element in database if instance does not exist in database,
        or update respective element if instance has existed in database.
        """
        pass

    def remove(self):
        """Remove instance from database."""
        pass

    def _update(self):
        pass

    def _create(self):
        pass
