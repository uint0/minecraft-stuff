import dataclasses

import preprocessors.models as models

@dataclasses.dataclass
class LogItem:
    time: str
    thread: str
    log_level: str
    payload: models.BaseMessage

@dataclasses.dataclass
class ForgeLogItem(LogItem):
    namespace: str

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