import pytest
from bdd import bddservice
from bdd.lesson import LessonType, ProgLang


def test_get_lesson_uuid_from_url_happy_path():
    url = "https://www.boot.dev/lessons/a011d7b7-209e-43ff-8d6a-aefa26e9772f"
    actual = bddservice.get_lesson_uuid_from_url(url)
    expected = "a011d7b7-209e-43ff-8d6a-aefa26e9772f"
    assert actual == expected


def test_get_lesson_uuid_from_url_handles_params():
    url = "https://www.boot.dev/lessons/abc-123?foo=bar"
    actual = bddservice.get_lesson_uuid_from_url(url)
    expected = "abc-123"
    assert actual == expected


def test_get_lesson_uuid_from_url_no_uuid():
    url = "https://www.boot.dev/lessons/"
    with pytest.raises(AssertionError):
        bddservice.get_lesson_uuid_from_url(url)


def test_get_lesson_uuid_from_url_too_long():
    url = "https://www.boot.dev/lessons/a011d7b7-209e-43ff-8d6a-aefa26e9772f/extra"
    with pytest.raises(AssertionError):
        bddservice.get_lesson_uuid_from_url(url)


mockWsMessageCorrect = '{"LessonSubmissionEvent":{"UserUUID":"e9c802e5-f8bd-44bc-becf-6128b14d4893","LessonUUID":"224252be-adc9-452f-8ed0-0b305b25d0cb","CourseUUID":"3b39d0f6-f944-4f1b-832d-a1daba32eda4","Err":null,"StructuredErrHTTPTest":null,"XPReward":null,"XPBreakdown":null}}'

mockWsMessageIncorrect = '{"LessonSubmissionEvent":{"UserUUID":"e9c802e5-f8bd-44bc-becf-6128b14d4893","LessonUUID":"224252be-adc9-452f-8ed0-0b305b25d0cb","CourseUUID":"3b39d0f6-f944-4f1b-832d-a1daba32eda4","Err":"Close! Your output is only a few characters off","StructuredErrHTTPTest":null,"XPReward":null,"XPBreakdown":null}}'

mockNotificationMessage = '{"NotificationCreated":{"UUID":"9a5957b9-4040-4dbe-bcad-809e38d8f39a","CreatedAt":"2024-08-09T02:41:30.304712Z","UpdatedAt":"2024-08-09T02:41:30.304712Z","UserUUID":"e9c802e5-f8bd-44bc-becf-6128b14d4893","NotificationType":"achievement_earned","EmailSentAt":null,"NotificationData":{"AchievementEarned":{"AchievementUUID":"85774747-64b5-422c-9964-49ff3ba433db","UserUUID":"e9c802e5-f8bd-44bc-becf-6128b14d4893","UnlockedAt":"2024-08-09T02:41:30.304375677Z","Title":"Milestone: Master","Description":"Complete 480 exercises","ImageURL":"https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/kyMPvAA.png","Category":"milestone","RewardAmount":0,"RewardType":"","Order":5,"PercentPlatformCompleted":3.2917182523556154},"DailyQuestEarned":null,"CertificateEarned":null,"BossEvent":null,"BossEventReward":null,"WeeklyStreakExpiry":null,"FrozenFlameConsumed":null,"ChestEarned":null},"NotificationViewedAt":null}}'


def test_lesson_submission_correct():
    def on_success(m):
        assert "Correct!" in m

    def on_error(_):
        pass

    parsed = bddservice.BddMessage.from_message(
        mockWsMessageCorrect, on_error=on_error, on_success=on_success
    )
    parsed.process()


def test_lesson_submission_incorrect():
    def on_success(_):
        pass

    def on_error(m):
        assert "[incorrect]: Close! Your output is" in m

    parsed = bddservice.BddMessage.from_message(
        mockWsMessageCorrect, on_error=on_error, on_success=on_success
    )
    parsed.process()


def test_parse_lesson_api_payload_malformed():
    payload = {}
    with pytest.raises(bddservice.LessonParsingError):
        bddservice.parse_lesson_api_payload(payload)


def test_parse_lesson_api_payload_code_go():
    payload = {
        "Lesson": {
            "CourseUUID": "3b39d0f6-f944-4f1b-832d-a1daba32eda4",
            "ChapterUUID": "a011d7b7-209e-43ff-8d6a-aefa26e9772f",
            "UUID": "224252be-adc9-452f-8ed0-0b305b25d0cb",
            "Type": "type_code",
            "LessonDataCodeCompletion": {
                "ProgLang": "go",
                "Readme": "This is a readme",
                "StarterFiles": [
                    {
                        "Name": "main.go",
                        "Content": 'package main\n\nimport "fmt"\n\nfunc main() {\n\tfmt.Println("Hello, World!")\n}',
                    },
                ],
            },
        }
    }
    lesson = bddservice.parse_lesson_api_payload(payload)
    assert lesson.course_uuid == "3b39d0f6-f944-4f1b-832d-a1daba32eda4"
    assert lesson.chapter_uuid == "a011d7b7-209e-43ff-8d6a-aefa26e9772f"
    assert lesson.uuid == "224252be-adc9-452f-8ed0-0b305b25d0cb"
    assert lesson.lesson_type == LessonType.CODE
    assert lesson.prog_lang == ProgLang.GO
    assert lesson.readme == "This is a readme"
    assert lesson.files == {
        "main.go": 'package main\n\nimport "fmt"\n\nfunc main() {\n\tfmt.Println("Hello, World!")\n}'
    }
