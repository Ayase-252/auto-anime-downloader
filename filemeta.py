class FileMeta:

    def __init__(self, name, ep, translation_team, url=''):
        self.name = name
        self.ep = ep
        self.translation_team = translation_team
        self.url = url

    def __eq__(self, other):
        if self.name == other.name and self.ep == other.ep \
           and self.translation_team == other.translation_team \
           and self.url == self.url:
            return True
        else:
            return False

    def __str__(self):
        return self.name + ' ' + str(self.ep) + ' ' \
            + str(self.translation_team) + ' ' + self.url
