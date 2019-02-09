# coding=utf-8
import sys
sys.path.append('../')

from log.log_processor import LogProcessor
from log.models import LogRow, PilotInfo

processor = LogProcessor()


def test_log_row_parsing():
    log_row = "23:49:08.277      038 – F.MASSA                           1		1:02.852                        44,275"
    row = processor.parse_row(log_row)
    assert row[0] == "23:49:08.277"
    assert row[1] == "038"
    assert row[2] == "F.MASSA"
    assert row[3] == "1"
    assert row[4] == "1:02.852"
    assert row[5] == "44,275"


def test_log_data_to_model():
    row = ["23:49:08.277", "038", "F.MASSA", "1", "1:02.852", "44,275"]
    row_model = LogRow(row)
    assert row_model.time == "23:49:08.277"
    assert row_model.pilot_id == 38
    assert row_model.pilot_name == "F.MASSA"
    assert row_model.lap_number == 1
    assert row_model.lap_time == "1:02.852"
    assert row_model.lap_av_speed == "44,275"


def test_log_parsing():
    rows = [
        "23:49:08.277      038 – F.MASSA                           1		1:02.852                        44,275",
        "23:49:08.277      039 – F.MASSA                           1		1:02.852                        44,275"
    ]
    result = processor.parse_log(rows)
    assert len(result) == 2
    assert result[0].pilot_id == 38
    assert result[1].pilot_id == 39


def test_read_pilots_data():
    rows = [
        LogRow(["23:49:08.277", "038", "F.MASSA", "1", "1:02.852", "44,275"]),
        LogRow(["23:49:10.858", "033", "R.BARRICHELLO", "1", "1:04.352", "43,243"]),
        LogRow(["23:49:11.075", "002", "K.RAIKKONEN", "1", "1:04.108", "43,408"]),
        LogRow(["23:49:30.976", "015", "F.ALONSO", "1", "1:18.456", "35,47"]),
        LogRow(["23:50:11.447", "038", "F.MASSA", "2", "1:03.170", "44,053"]),
        LogRow(["23:50:14.860", "033", "R.BARRICHELLO", "2", "1:04.002", "43,48"])
    ]
    pilots = processor.process_log(rows)
    assert len(pilots.keys()) == 4
    assert len(pilots[38]) == 2
    assert len(pilots[33]) == 2
    assert len(pilots[2]) == 1
    assert len(pilots[15]) == 1


def test_parse_time():
    time = "1:02.500"
    parsed = processor.parse_time(time)
    assert parsed.microseconds == 500000
    assert parsed.seconds == 62


def test_race_duration():
    logs = [
        LogRow(["", "0", "", "1", "1:00.000", ""]),
        LogRow(["", "0", "", "2", "1:00.000", ""]),
        LogRow(["", "0", "", "3", "1:00.000", ""]),
    ]
    duration = processor.compute_race_duration(logs)
    assert duration.seconds == 180


def test_compute_pilots_position():
    pilots_data = [
        PilotInfo([
            LogRow(["", "01", "a", "1", "0:43.000", ""]),
            LogRow(["", "01", "a", "2", "0:43.000", ""]),
            LogRow(["", "01", "a", "3", "0:44.000", ""]),
        ], "2:10.000"),
        PilotInfo([
            LogRow(["", "02", "b", "1", "0:30.000", ""]),
            LogRow(["", "02", "b", "2", "0:30.000", ""]),
        ], "1:00.000"),
        PilotInfo([
            LogRow(["", "03", "c", "1", "0:40.000", ""]),
            LogRow(["", "03", "c", "2", "0:40.000", ""]),
            LogRow(["", "03", "c", "3", "0:40.000", ""]),
        ], "2:00.000"),
    ]
    processor.compute_each_pilot_position(pilots_data)
    assert pilots_data[0].pilot_id == 03 and pilots_data[0].position == 1
    assert pilots_data[1].pilot_id == 01 and pilots_data[1].position == 2
    assert pilots_data[2].pilot_id == 02 and pilots_data[2].position == 3


def test_log_file_reading():
    file_path = "test_input.txt"
    result = processor.parse_log_file(file_path)
    assert result.len() == 23
    assert len(result.pilots_data) == 6


test_log_row_parsing()
test_log_data_to_model()
test_log_parsing()
test_read_pilots_data()
test_parse_time()
test_race_duration()
test_compute_pilots_position()
test_log_file_reading()
print "all tests passed"
