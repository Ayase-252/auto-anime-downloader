import unittest

from anime.anime_manager import AnimeManager
from anime.anime import Anime

class AnimeManagerTest(unittest.TestCase):
    def test_add_new_anime(self):
        anime_manager = AnimeManager()
        anime_manager.write(name='Your name', total_episode=1,
                            start_date='2016-01-01')
        anime_manager.set_factory(Anime.__init__)
        anime = anime_manager.read(name='Your name')
        self.assertEqual(anime.name, 'Your name')
        self.assertEqual(anime.downloaded_episodes, [])
        self.assertEqual(anime.start_date, '2016-01-01')
