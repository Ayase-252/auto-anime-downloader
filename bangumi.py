from datetime import date


class Bangumi:

    def __init__(self, name, start_date, translation_team=[],
                 downloaded_ep=0, total_ep=0, offset=0):
        self.name = name
        self.start_date = start_date
        self.translation_team = translation_team
        self.downloaded_ep = cached_ep
        self.total_ep = total_ep
        self.offset = offset
