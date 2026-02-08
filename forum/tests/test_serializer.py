from django.test import TestCase
from forum.models import Question, UserProfile, Answer, QuestionVote, AnswerVote, Report
from forum.serializers import QuestionSerializer, UserSerializer, UserProfileSerializer, AnswerSerializer, QuestionVoteSerializer, AnswerVoteSerializer, ReportSerializer
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import AnonymousUser

class QuestionSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='seruser', password='testpass')
        UserProfile.objects.create(user=self.user, role='USER')
        self.question = Question.objects.create(title='Q', content='C', created_by=self.user)
        self.factory = APIRequestFactory()

    def test_question_serializer(self):
        request = self.factory.get('/')
        request.user = self.user  # Add user to request
        serializer = QuestionSerializer(instance=self.question, context={'request': request})
        data = serializer.data
        self.assertEqual(data['title'], 'Q')
        self.assertEqual(data['content'], 'C')

class UserSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='usertest', password='testpass', email='user@example.com')

    def test_user_serializer_valid(self):
        serializer = UserSerializer(instance=self.user)
        self.assertEqual(serializer.data['username'], 'usertest')
        self.assertEqual(serializer.data['email'], 'user@example.com')
        self.assertNotIn('oldpassword', serializer.data)

    def test_user_serializer_password_validation(self):
        data = {'username': 'newuser', 'email': 'new@example.com', 'password': 'short', 'oldpassword': 'testpass'}
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

class UserProfileSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='profileuser', password='testpass')

    def test_userprofile_serializer(self):
        profile = UserProfile.objects.create(user=self.user, role='USER')
        serializer = UserProfileSerializer(instance=profile)
        self.assertEqual(serializer.data['role'], 'USER')

class AnswerSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='auser', password='testpass')
        self.question = Question.objects.create(title='Q', content='C', created_by=self.user)
        self.answer = Answer.objects.create(question=self.question, body='Body', answered_by=self.user)

    def test_answer_serializer(self):
        serializer = AnswerSerializer(instance=self.answer)
        self.assertEqual(serializer.data['body'], 'Body')
        self.assertEqual(serializer.data['answered_by'], 'auser')

class QuestionVoteSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='vuser', password='testpass')
        self.question = Question.objects.create(title='Q', content='C', created_by=self.user)
        self.factory = APIRequestFactory()
        self.request = self.factory.post('/')
        self.request.user = self.user

    def test_vote_serializer_valid(self):
        data = {'question': self.question.id, 'vote_type': 'LIKE'}
        serializer = QuestionVoteSerializer(data=data, context={'request': self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)

class AnswerVoteSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='avuser', password='testpass')
        self.question = Question.objects.create(title='Q', content='C', created_by=self.user)
        self.answer = Answer.objects.create(question=self.question, body='Body', answered_by=self.user)
        self.factory = APIRequestFactory()
        self.request = self.factory.post('/')
        self.request.user = self.user

    def test_answervote_serializer_valid(self):
        data = {'answer': self.answer.id, 'vote_type': 'LIKE'}
        serializer = AnswerVoteSerializer(data=data, context={'request': self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertIn('create_at', serializer.fields)

class ReportSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ruser', password='testpass')
        self.question = Question.objects.create(title='Q', content='C', created_by=self.user)
        self.report = Report.objects.create(question=self.question, user=self.user, status='PENDING')

    def test_report_serializer(self):
        serializer = ReportSerializer(instance=self.report)
        self.assertEqual(serializer.data['status'], 'PENDING')
        self.assertEqual(serializer.data['question_title'], 'Q')