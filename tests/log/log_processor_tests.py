# coding=utf-8
from src.log.log_processor import LogProcessor, LogRow


def test_log_row_parsing():
    log_row = "23:49:08.277      038 – F.MASSA                           1		1:02.852                        44,275"
    row = LogProcessor.parse_row(log_row)
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


test_log_row_parsing()
test_log_data_to_model()
