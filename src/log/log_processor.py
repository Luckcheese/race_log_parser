# coding=utf-8
from src.log.models import Log, LogRow


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

    def parse_log_file(self, log_file):
        log = open(log_file, "r")
        next(log)
        logs = self.parse_log(log)
        pilots_data = self.process_log(logs)
        return Log(logs, pilots_data)
