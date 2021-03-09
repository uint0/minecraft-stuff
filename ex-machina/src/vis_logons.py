import preprocessor
import preprocessors.models
import util
import sys

binned_times = [0] * 24

for event in preprocessor.process_logs(sys.argv[1], processor=preprocessor.PROCESSOR_FORGE):
    if isinstance(event.payload, preprocessors.models.ConnectionMessage):
        binned_times[util.utc_to_local(event.time).hour] += 1

for i, c in enumerate(binned_times):
    print(f'{str(i).zfill(2)}:00 - {str(i).zfill(2)}:59 ->\t{c} login')