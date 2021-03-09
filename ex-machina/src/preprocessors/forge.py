import re
import io
import typing
import datetime as dt
import preprocessors.common as common

def process_base_log_stream(stream: io.TextIOWrapper) -> typing.Iterable[dict]:
    matcher = re.compile(r"^\[(?P<time>.+)\] \[(?P<thread>[^\/]+)\/(?P<log_level>[A-Z]+)\] \[(?P<namespace>[^\/]+\/[^\]]*)\]:\s*(?P<message>.*)$")
    for line in stream:
        if len(line.strip()) == 0: continue
        matches = re.match(matcher, line.strip())

        if matches is None:
            print('[WARN] Did not find a match on line, may be a multiline log which is currently unsupported')
            continue

        yield matches.groupdict()

def process_message(message: str):
    return common.process_message(message)

def process_log_file(stream: io.TextIOWrapper) -> typing.Iterable[common.LogItem]:
    for entry in process_base_log_stream(stream):
        yield common.ForgeLogItem(
            time=dt.datetime.strptime(entry['time'], '%d%b%Y %H:%M:%S.%f'),
            thread=entry['thread'],
            log_level=entry['log_level'],
            namespace=entry['namespace'],
            payload=process_message(entry['message'])
        )