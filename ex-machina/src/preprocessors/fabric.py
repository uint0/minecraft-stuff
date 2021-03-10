import re
import io
import typing
import datetime as dt
import preprocessors.models as models
import preprocessors.common as common

def process_base_log_stream(stream: io.TextIOWrapper) -> typing.Iterable[dict]:
    matcher = re.compile(r"^\[(?P<time>.+)\] \[(?P<thread>[^\/]+)\/(?P<log_level>[A-Z]+)\]: (?P<message>.+)$")
    for line in stream:
        yield re.match(matcher, line.strip()).groupdict()

def process_message(message: str):
    return common.process_message(message)

def process_log_file(stream: io.TextIOWrapper) -> typing.Iterable[common.LogItem]:
    for entry in process_base_log_stream(stream):
        yield common.LogItem(
            time=dt.datetime.strptime(f"{'-'.join(stream.name.split('-')[:3])}T{entry['time']}", "%Y-%B-%dT%H:%M:%S"),
            thread=entry['thread'],
            log_level=entry['log_level'],
            payload=process_message(entry['message'])
        )
