import preprocessor
import preprocessors.models
import util
import sys
import dateutil.rrule

binned_times = [0] * 24
sessions = {}

for event in preprocessor.process_logs(sys.argv[1], processor=preprocessor.PROCESSOR_FORGE):
    if isinstance(event.payload, preprocessors.models.ConnectionMessage):
        sessions[event.payload.player] = event
    elif isinstance(event.payload, preprocessors.models.DisconnectionMessage):
        assoc_signin = sessions[event.payload.player]

        start = util.utc_to_local(assoc_signin.time)
        end   = util.utc_to_local(event.time)

        print(event.payload.player, start, end)
        for hour_tick in dateutil.rrule.rrule(dateutil.rrule.HOURLY, dtstart=start, until=end):
            binned_times[hour_tick.hour] += 1

for i, c in enumerate(binned_times):
    print(f'{str(i).zfill(2)}:00 - {str(i).zfill(2)}:59 ->\t{c} times online')