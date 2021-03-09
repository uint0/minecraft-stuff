import re
import io
import typing
from collections import namedtuple
import models

LogItem = namedtuple('LogItem', ['time', 'thread', 'log_level', 'payload'])

def process_base_log_stream(stream: io.TextIOWrapper) -> typing.Iterable[dict]:
    matcher = re.compile(r"^\[(?P<time>.+)\] \[(?P<thread>[^\/]+)\/(?P<log_level>[A-Z]+)\]: (?P<message>.+)$")
    for line in stream:
        yield re.match(matcher, line.strip()).groupdict()

def process_message(message: str):
    matching_models = [
        models.ConnectionMessage,
        models.DisconnectionMessage,
        models.LagMessage,
        models.BaseMessage
    ]

    for matcher in matching_models:
        if m := matcher.from_match(message):
            return m

    raise RuntimeError(f"Message [{message}] was not matched by any matcher - including BaseMessage!")

def process_log_file(stream: io.TextIOWrapper) -> typing.Iterable[LogItem]:
    for entry in process_base_log_stream(stream):
        yield LogItem(
            time=entry['time'],  # TODO: get date
            thread=entry['thread'],
            log_level=entry['log_level'],
            payload=process_message(entry['message'])
        )

if __name__ == '__main__':
    for entry in process_log_file(open('tests/test.log')):
        print(entry)
        
