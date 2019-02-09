# coding=utf-8
from models import Log, LogRow, PilotInfo
from datetime import timedelta
from operator import attrgetter


class LogProcessor:

    def __init__(self):
        pass

    @staticmethod
    def parse_row(row):
        all_fields = row.replace("\t", " ").split(" ")
        filtered_fields = filter(lambda f: len(f) > 0 and f != "–", all_fields)
        return filtered_fields

    def parse_log(self, log_data):
        rows = map(lambda r: self.parse_row(r), log_data)
        return map(lambda r: LogRow(r), rows)

    @staticmethod
    def process_log(log_rows):
        agg = {}
        for row in log_rows:
            if row.pilot_id in agg.keys():
                agg[row.pilot_id].append(row)
            else:
                agg[row.pilot_id] = [row]
        return agg

    @staticmethod
    def parse_time(time):
        time_fields = time.replace(".", ":").split(":")
        time_fields = map(lambda x: int(x), time_fields)
        time_fields.reverse()
        if len(time_fields) == 3:
            time_fields.append(0)
        return timedelta(
            milliseconds=time_fields[0],
            seconds=time_fields[1],
            minutes=time_fields[2],
            hours=time_fields[3]
        )

    @staticmethod
    def compute_race_duration(pilot_data):
        laps_time_str = map(lambda x: x.lap_time, pilot_data)
        laps_time = map(lambda x: LogProcessor.parse_time(x), laps_time_str)
        return reduce(lambda x, y: x + y, laps_time)

    @staticmethod
    def pilot_log_to_model(log):
        race_duration = LogProcessor.compute_race_duration(log)
        return PilotInfo(log, race_duration)

    @staticmethod
    def compute_each_pilot_position(pilots_data):
        pilots_data.sort(key=attrgetter('race_duration'))
        pilots_data.sort(key=attrgetter('completed_laps'), reverse=True)
        for index, data in enumerate(pilots_data):
            data.position = index + 1
        return pilots_data

    @staticmethod
    def check_if_any_pilot_completed_the_race(pilots_data):
        race_ended = False
        for data in pilots_data:
            if data.completed_laps == 4:
                race_ended = True
        return race_ended

    def parse_log_file(self, log_file):
        log = open(log_file, "r")
        next(log)
        logs = self.parse_log(log)
        pilots_logs = self.process_log(logs)
        pilots_data = map(lambda x: LogProcessor.pilot_log_to_model(x), pilots_logs.itervalues())
        pilots_data = LogProcessor.compute_each_pilot_position(pilots_data)
        race_ended = self.check_if_any_pilot_completed_the_race(pilots_data)
        return Log(logs, pilots_data, race_ended)
