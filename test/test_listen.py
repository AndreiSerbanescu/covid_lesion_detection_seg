import mock
from listen import *


# @mock.patch('time.time')
# @mock.patch('subprocess.call')
# def test_seg_muscle_calls_time_once(mock_call, mock_time):
#
#     mock_time_value = "123.123"
#     mock_time.return_value = mock_time_value
#     param_dict = {"source_file": ["/source/dir"]}
#     segment_muscle(param_dict)
#     mock_time.assert_called_once()
#
@mock.patch('time.time')
@mock.patch('subprocess.call')
def test_lesion_detection_calls_sb_call_four_times(mock_call, mock_time):

    mock_time_value = "123.123"
    mock_time.return_value = mock_time_value
    param_dict = {"source_file": ["/source/dir"]}
    mock_call.return_Value = 0

    covid_detector_seg(param_dict)

    assert mock_call.call_count == 4
#
#
# @mock.patch('time.time')
# @mock.patch('subprocess.call')
# def test_seg_muscle_sends_success_true_if_subprocess_exits_with_zero(mock_call, mock_time):
#
#     mock_time_value = "123.123"
#     mock_time.return_value = mock_time_value
#     param_dict = {"source_file": ["/source/dir"]}
#     mock_call.return_value = 0
#
#     result_dict, success = segment_muscle(param_dict)
#
#     assert success
#
#
# @mock.patch('time.time')
# @mock.patch('subprocess.call')
# def test_seg_muscle_sends_success_false_if_subprocess_segment_exits_with_one(mock_call, mock_time):
#
#     mock_time_value = "123.123"
#     mock_time.return_value = mock_time_value
#     param_dict = {"source_file": ["/source/dir"]}
#     mock_call.side_effect = [1, 0]
#
#     result_dict, success = segment_muscle(param_dict)
#
#     assert not success
#
# @mock.patch('time.time')
# @mock.patch('subprocess.call')
# def test_seg_muscle_sends_success_false_if_subprocess_move_exits_with_one(mock_call, mock_time):
#
#     mock_time_value = "123.123"
#     mock_time.return_value = mock_time_value
#     param_dict = {"source_file": ["/source/dir"]}
#     mock_call.side_effect = [0, 1]
#
#     result_dict, success = segment_muscle(param_dict)
#
#     assert not success
#
# @mock.patch('time.time')
# @mock.patch('subprocess.call')
# def test_seg_muscle_result_dict_contains_segmentation(mock_call, mock_time):
#
#     mock_time_value = "123.123"
#     mock_time.return_value = mock_time_value
#     param_dict = {"source_file": ["/source/dir"]}
#     mock_call.return_value = 0
#
#     result_dict, success = segment_muscle(param_dict)
#
#     assert "segmentation" in result_dict