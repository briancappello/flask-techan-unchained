from enum import Enum, EnumMeta


class ByNameAndValueEnumMeta(EnumMeta):
    def __getitem__(self, name):
        try:
            return self._member_map_[name]
        except KeyError:
            return self._value2member_map_[name]


class AssetType(Enum):
    Asset = 'Asset'
    Equity = 'Equity'


class Frequency(Enum, metaclass=ByNameAndValueEnumMeta):
    Minutely = '1min'
    FiveMinutely = '5min'
    TenMinutely = '10min'
    FifteenMinutely = '15min'
    ThirtyMinutely = '30min'
    Hourly = '1hr'
    Daily = 'D'
    Weekly = 'W'
    Monthly = 'M'
    Yearly = 'Y'
