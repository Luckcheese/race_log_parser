# coding=utf-8


class LogRow:

    def __init__(self, data):
        self.time = data[0]
        self.pilot_id = int(data[1])
        self.pilot_name = data[2]
        self.lap_number = int(data[3])
        self.lap_time = data[4]
        self.lap_av_speed = data[5]

    def __str__(self):
        return """time: %s | pilotId: %d | pilotName: %s | lapNumber: %d | lapTime: %s | lapAvSpeed: %s""" % \
               (self.time, self.pilot_id, self.pilot_name, self.lap_number, self.lap_time, self.lap_av_speed)


class PilotInfo:

    def __init__(self, log_rows, race_duration):
        assert len(log_rows) > 0
        self.log_rows = log_rows
        self.pilot_id = log_rows[0].pilot_id
        self.pilot_name = log_rows[0].pilot_name
        self.completed_laps = len(log_rows)
        self.race_duration = race_duration
        self.position = 0

    def __str__(self):
        return """%.2d \t %.3d - %s \t\t %.2d \t %s""" % \
               (self.position, self.pilot_id, self.pilot_name, self.completed_laps, self.race_duration)

class Log:

    def __init__(self, log, pilots_data):
        self.rows = log
        self.pilots_data = pilots_data

    def len(self):
        return len(self.rows)
