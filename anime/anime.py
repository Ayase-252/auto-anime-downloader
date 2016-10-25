"""Anime model."""

from datetime import datetime


class Anime:
    """Anime model.

    Attributes:
        name: Name of anime(Required).
        start_day: Day when anime premires(Required).
        total_episode: Total episodes.
        downloaded_episodes: Episode which have been downloaded.
    """

    def __init__(self, name, start_day, total_episode=99,
                 downloaded_episodes=None):
        """Initial an anime instance.

        Args refers to class docstring.
        """
        self.name = name
        self.start_day = start_day
        self.total_episode = total_episode
        if downloaded_episodes is None:
            self.downloaded_episodes = []
        else:
            self.downloaded_episodes = downloaded_episodes

    def add_downloaded_episode(self, downloaded_episode):
        """Add downloaded episode into record.
        """
        self.downloaded_episodes.append(downloaded_episode)

    def get_downloaded_episodes(self):
        """Return a list of downloaded episodes
        """
        return self.downloaded_episodes

    def get_avaliable_episodes(self, current_date):
        """Return a list of avaliable episodes that have not been downloaded.
        """
        airing_episode = self._calculate_latest_episode(current_date)
        avaliable_episode = []
        for i in range(1, airing_episode):
            if i not in self.downloaded_episodes:
                avaliable_episode.append(i)
        return avaliable_episode

    def _calculate_latest_episode(self, current_date):
        """Calculates latest episode which is on airing.
        """
        current_date = _convert_datestring(current_date)
        start_date = _convert_datestring(self.start_day)
        return min((current_date - start_date).days // 7 + 1,
                   self.total_episode + 1)


def _convert_datestring(datestring):
    """Convert string in format of '%Y-%m-%d' (e.g 2016-08-03) to a
    date object
    """
    return datetime.strptime(datestring, '%Y-%m-%d').date()
