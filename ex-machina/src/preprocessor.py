import re
import os
import datetime as dt
import typing

import preprocessors.common
import preprocessors.fabric
import preprocessors.forge


PROCESSOR_FABRIC = preprocessors.fabric
PROCESSOR_FORGE = preprocessors.forge

def is_valid_log_filename(filename):
    return re.match(r"^\d{4}-\d{2}-\d{2}(-\d+)?\.log$", filename) is not None

def process_logs(
    logs_loc: str,
    /,
    processor=PROCESSOR_FABRIC,
    ordering_key: typing.Callable=lambda filename: filename
) -> typing.Iterator[preprocessors.common.ForgeLogItem]:
    """
    Given a path to a directory of logs process each log file sequentially
    """

    if not os.path.isdir(logs_loc):
        raise ValueError("Provided location isn't a directory")

    processor_requires_filename = [PROCESSOR_FABRIC]

    logs = os.listdir(logs_loc)

    for logfile in sorted(logs, key=ordering_key):
        if processor in processor_requires_filename and not is_valid_log_filename(logfile):
            print(f"{logfile} is not a valid logfile name, skipping...")
            continue

        with open(os.path.join(logs_loc, logfile), 'r') as f:
            yield from processor.process_log_file(f)

if __name__ == '__main__':
    import sys
    for item in process_logs(sys.argv[1], processor=PROCESSOR_FORGE):
        print(item)

