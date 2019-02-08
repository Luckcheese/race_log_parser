# coding=utf-8
from src.log.log_processor import LogProcessor
from src.log.models import LogRow

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


def test_log_file_reading():
    file_path = "test_input.txt"
    result = processor.parse_log_file(file_path)
    assert result.len() == 23


test_log_row_parsing()
test_log_data_to_model()
test_log_parsing()
test_log_file_reading()
