import datetime as dt
import dateutil.tz

def utc_to_local(utc_datetime: dt.datetime) -> dt.datetime:
    return utc_datetime \
        .replace(tzinfo=dateutil.tz.tzutc()) \
        .astimezone(dateutil.tz.tzlocal())
