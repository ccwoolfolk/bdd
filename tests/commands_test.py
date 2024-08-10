import pytest

from bdd.commands import BddMessage

mockWsMessageCorrect = '{"LessonSubmissionEvent":{"UserUUID":"e9c802e5-f8bd-44bc-becf-6128b14d4893","LessonUUID":"224252be-adc9-452f-8ed0-0b305b25d0cb","CourseUUID":"3b39d0f6-f944-4f1b-832d-a1daba32eda4","Err":null,"StructuredErrHTTPTest":null,"XPReward":null,"XPBreakdown":null}}'

mockWsMessageIncorrect = '{"LessonSubmissionEvent":{"UserUUID":"e9c802e5-f8bd-44bc-becf-6128b14d4893","LessonUUID":"224252be-adc9-452f-8ed0-0b305b25d0cb","CourseUUID":"3b39d0f6-f944-4f1b-832d-a1daba32eda4","Err":"Close! Your output is only a few characters off","StructuredErrHTTPTest":null,"XPReward":null,"XPBreakdown":null}}'

mockNotificationMessage = '{"NotificationCreated":{"UUID":"9a5957b9-4040-4dbe-bcad-809e38d8f39a","CreatedAt":"2024-08-09T02:41:30.304712Z","UpdatedAt":"2024-08-09T02:41:30.304712Z","UserUUID":"e9c802e5-f8bd-44bc-becf-6128b14d4893","NotificationType":"achievement_earned","EmailSentAt":null,"NotificationData":{"AchievementEarned":{"AchievementUUID":"85774747-64b5-422c-9964-49ff3ba433db","UserUUID":"e9c802e5-f8bd-44bc-becf-6128b14d4893","UnlockedAt":"2024-08-09T02:41:30.304375677Z","Title":"Milestone: Master","Description":"Complete 480 exercises","ImageURL":"https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/kyMPvAA.png","Category":"milestone","RewardAmount":0,"RewardType":"","Order":5,"PercentPlatformCompleted":3.2917182523556154},"DailyQuestEarned":null,"CertificateEarned":null,"BossEvent":null,"BossEventReward":null,"WeeklyStreakExpiry":null,"FrozenFlameConsumed":null,"ChestEarned":null},"NotificationViewedAt":null}}'


def test_lesson_submission_correct():
    def on_success(m):
        assert "Correct!" in m

    def on_error(_):
        pass

    parsed = BddMessage.from_message(
        mockWsMessageCorrect, on_error=on_error, on_success=on_success
    )
    parsed.process()


def test_lesson_submission_incorrect():
    def on_success(_):
        pass

    def on_error(m):
        assert "[incorrect]: Close! Your output is" in m

    parsed = BddMessage.from_message(
        mockWsMessageCorrect, on_error=on_error, on_success=on_success
    )
    parsed.process()
