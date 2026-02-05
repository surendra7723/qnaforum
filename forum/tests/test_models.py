
from django.test import TestCase
from django.contrib.auth.models import User
from forum.models import UserProfile, Question, Answer

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
