from django.test import TestCase
from django.contrib.auth.models import User
from forum.models import UserProfile, Question, Answer, QuestionVote, AnswerVote, Report
from django.utils import timezone

class UserProfileModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='testuser', password='testpass')

	def test_profile_creation(self):
		profile = UserProfile.objects.create(user=self.user)
		self.assertEqual(profile.role, 'USER')
		self.assertEqual(profile.user.username, 'testuser')

class QuestionModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='questionuser', password='testpass')

	def test_question_creation(self):
		question = Question.objects.create(title='Test Q', content='Test Content', created_by=self.user)
		self.assertEqual(question.status, 'PENDING')
		self.assertEqual(question.title, 'Test Q')
		self.assertEqual(question.created_by.username, 'questionuser')

class AnswerModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='answeruser', password='testpass')
		self.question = Question.objects.create(title='Test Q', content='Test Content', created_by=self.user)

	def test_answer_creation(self):
		answer = Answer.objects.create(question=self.question, body='Test Answer', answered_by=self.user)
		self.assertEqual(answer.body, 'Test Answer')
		self.assertEqual(answer.question, self.question)
		self.assertEqual(answer.answered_by.username, 'answeruser')

class QuestionVoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='voteuser', password='testpass')
        self.question = Question.objects.create(title='Vote Q', content='Vote Content', created_by=self.user)

    def test_vote_creation(self):
        vote = QuestionVote.objects.create(question=self.question, voter=self.user, vote_type='LIKE')
        self.assertEqual(vote.vote_type, 'LIKE')
        self.assertEqual(str(vote), f"vote for {self.question.id} by {self.user.username}")

class AnswerVoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='avoteuser', password='testpass')
        self.question = Question.objects.create(title='A Q', content='A Content', created_by=self.user)
        self.answer = Answer.objects.create(question=self.question, body='A', answered_by=self.user)

    def test_answer_vote_creation(self):
        avote = AnswerVote.objects.create(answer=self.answer, voter=self.user, vote_type='DISLIKE')
        self.assertEqual(avote.vote_type, 'DISLIKE')
        self.assertEqual(str(avote), f"vote on answer {self.answer.id} by {self.user.username}")

class ReportModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reportuser', password='testpass')
        self.question = Question.objects.create(title='Report Q', content='Report Content', created_by=self.user)

    def test_report_creation_and_str(self):
        report = Report.objects.create(question=self.question, user=self.user, status='PENDING')
        self.assertEqual(report.status, 'PENDING')
        self.assertEqual(str(report), f"Report on Question {self.question.id} for {self.user} ")

    def test_report_approve_sets_question_status(self):
        report = Report.objects.create(question=self.question, user=self.user, status='PENDING')
        report.status = 'APPROVED'
        report.save()
        self.question.refresh_from_db()
        self.assertEqual(self.question.status, 'APPROVED')

class QuestionMethodsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='methoduser', password='testpass')
        self.question = Question.objects.create(title='Q', content='C', created_by=self.user)

    def test_total_likes_and_dislikes(self):
        QuestionVote.objects.create(question=self.question, voter=self.user, vote_type='LIKE')
        self.assertEqual(self.question.total_likes, 1)
        self.assertEqual(self.question.total_dislikes, 0)

    def test_str(self):
        self.assertIn('Question:', str(self.question))

class AnswerMethodsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='amethoduser', password='testpass')
        self.question = Question.objects.create(title='Q', content='C', created_by=self.user)
        self.answer = Answer.objects.create(question=self.question, body='B', answered_by=self.user)

    def test_str(self):
        self.assertIn('answer for', str(self.answer))
