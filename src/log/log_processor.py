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
        logs = map(lambda r: LogRow(r), rows)
        return Log(logs)

    def parse_log_file(self, log_file):
        log = open(log_file, "r")
        next(log)
        return self.parse_log(log)
