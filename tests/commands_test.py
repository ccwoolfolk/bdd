import pytest

from bdd.commands import get_error_from_wss_message

mockWsMessageCorrect = '{"LessonSubmissionEvent":{"UserUUID":"e9c802e5-f8bd-44bc-becf-6128b14d4893","LessonUUID":"224252be-adc9-452f-8ed0-0b305b25d0cb","CourseUUID":"3b39d0f6-f944-4f1b-832d-a1daba32eda4","Err":null,"StructuredErrHTTPTest":null,"XPReward":null,"XPBreakdown":null}}'

mockWsMessageIncorrect = '{"LessonSubmissionEvent":{"UserUUID":"e9c802e5-f8bd-44bc-becf-6128b14d4893","LessonUUID":"224252be-adc9-452f-8ed0-0b305b25d0cb","CourseUUID":"3b39d0f6-f944-4f1b-832d-a1daba32eda4","Err":"Close! Your output is only a few characters off","StructuredErrHTTPTest":null,"XPReward":null,"XPBreakdown":null}}'


def test_get_error_from_wss_message_correct():
    actual = get_error_from_wss_message(mockWsMessageCorrect)
    assert actual is None


def test_get_error_from_wss_message_incorrect():
    actual = get_error_from_wss_message(mockWsMessageIncorrect)
    assert actual == "Close! Your output is only a few characters off"
