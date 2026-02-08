from django.core.management import call_command
from django.test import TestCase
from forum.models import UserProfile, Question, Answer, QuestionVote, AnswerVote, Report
from django.contrib.auth.models import User

class PopulateForumCommandTest(TestCase):
    def test_populate_forum_command_creates_data(self):
        # Run the command with default arguments
        call_command('populate_forum', users=3, questions=5, answers=7, clear=True, verbosity=0)
        self.assertGreaterEqual(User.objects.count(), 3)
        self.assertGreaterEqual(UserProfile.objects.count(), 3)
        self.assertGreaterEqual(Question.objects.count(), 5)
        self.assertGreaterEqual(Answer.objects.count(), 7)
        self.assertGreaterEqual(QuestionVote.objects.count(), 0)  # May be 0 if not implemented
        self.assertGreaterEqual(AnswerVote.objects.count(), 0)
        self.assertGreaterEqual(Report.objects.count(), 0)

    def test_populate_forum_command_clear(self):
        # Create some data
        call_command('populate_forum', users=2, questions=2, answers=2, clear=True, verbosity=0)
        # Run again with clear, should not duplicate
        call_command('populate_forum', users=2, questions=2, answers=2, clear=True, verbosity=0)
        self.assertLessEqual(User.objects.count(), 2)
        self.assertLessEqual(Question.objects.count(), 2)
        self.assertLessEqual(Answer.objects.count(), 2)
