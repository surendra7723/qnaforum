from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from forum.models import Question, UserProfile

class QuestionAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='apiuser', password='testpass')
        UserProfile.objects.create(user=self.user, role='USER')
        self.client.force_authenticate(user=self.user)
        self.question = Question.objects.create(title='Q', content='C', created_by=self.user)

    def test_question_list(self):
        url = reverse('question-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)