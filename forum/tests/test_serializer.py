from django.test import TestCase
from forum.models import Question, UserProfile
from forum.serializers import QuestionSerializer
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