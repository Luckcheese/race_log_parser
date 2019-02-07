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
        return """
            time: %s | pilotId: %d | pilotName: %s | lapNumber: %d | lapTime: %s | lapAvSpeed: %s
        """ % (self.time, self.pilot_id, self.pilot_name, self.lap_number, self.lap_time, self.lap_av_speed)


class LogProcessor:

    def __init__(self):
        pass

    @staticmethod
    def parse_row(row):
        all_fields = row.replace("\t", " ").split(" ")
        filtered_fields = filter(lambda f: len(f) > 0 and f != "–", all_fields)

        return filtered_fields