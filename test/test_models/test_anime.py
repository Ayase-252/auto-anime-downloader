import unittest

from models.anime import Anime

class AnimeTest(unittest.TestCase):
    def test_initial_anime(self):
        anime = Anime(name='hello test', total_episode=12, start_day='2016-07-09')
        self.assertEqual(anime.name, 'hello test')
        self.assertEqual(anime.total_episode, 12)
        self.assertEqual(anime.start_day, '2016-07-09')

    def test_initial_partial_downloaded_anime(self):
        anime = Anime(name='hello test', total_episode=12, downloaded_episodes=[1,2],
                start_day='2016-08-02')
        self.assertEqual(anime.name, 'hello test')
        self.assertEqual(anime.total_episode, 12)
        self.assertEqual(anime.get_downloaded_episodes(), [1, 2])
        self.assertEqual(anime.start_day, '2016-08-02')

    def test_anime_add_downloaded_episode(self):
        anime = Anime(name='hello test', total_episode=12, start_day='2016-07-09')
        anime.add_downloaded_episode(1)
        self.assertEqual(anime.get_downloaded_episodes(),[1])

    def test_get_available_episode(self):
        anime = Anime(name='hello test', total_episode=12, start_day='2016-10-07')
        self.assertEqual(anime.get_avaliable_episodes('2016-10-14'),[1])

    def test_get_available_episode_when_anime_has_not_been_on_air(self):
        anime = Anime(name='hello test', total_episode=12, start_day='2019-10-20')
        self.assertEqual(anime.get_avaliable_episodes('2016-10-14'),[])

    def test_get_available_episode_when_anime_has_finished_airing(self):
        anime = Anime(name='hello test', total_episode=3, start_day='2015-09-23')
        self.assertEqual(anime.get_avaliable_episodes('2016-10-14'),[1, 2, 3])

    def test_W0102_bug(self):
        anime1 = Anime(name='1', total_episode=99, start_day='2016-07-10')
        anime2 = Anime(name='2', total_episode=99, start_day='2016-07-10')
        anime1.add_downloaded_episode(1)
        anime2.add_downloaded_episode(1)
        self.assertEqual(anime1.get_downloaded_episodes() ,[1])
        self.assertEqual(anime2.get_downloaded_episodes() ,[1])
