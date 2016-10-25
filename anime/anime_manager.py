"""Anime Manager
"""
import json
from pathlib import Path

class AnimeManager:
    def __init__(self):
        path = Path('anime.db')
        self._anime_factory = None
        if path.is_file():
            fp = open('anime.db', encoding='utf-8')
            self.records = json.loads(fp)


    def write(self, name, total_episode, start_date, downloaded_episodes=None):
        """Add a anime record.
        Args:
        name
        total_episode
        downloaded_episodes
        start_date
        """
        pass

    def read(self, name):
        """Read a record
        """
        pass

    def set_factory(self, factory):
        """
        """
        self._anime_factory = factory
