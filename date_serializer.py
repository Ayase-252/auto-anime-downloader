from datetime import date, datetime

from tinydb_serialization import Serializer


class DateSerializer(Serializer):
    OBJ_CLASS = date

    def encode(self, obj):
        return obj.strftime('%Y-%m-%d')

    def decode(self, s):
        return datetime.strptime(s, '%Y-%m-%d').date()
