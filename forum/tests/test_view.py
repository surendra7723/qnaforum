from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from forum.models import Question, UserProfile, Answer, QuestionVote, Report
from rest_framework import status

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

    def test_question_create(self):
        url = reverse('question-list')
        data = {'title': 'New Q', 'content': 'New Content'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Q')

    def test_question_detail(self):
        url = reverse('question-detail', args=[self.question.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Q')

    def test_question_delete_own_pending(self):
        url = reverse('question-detail', args=[self.question.id])
        response = self.client.delete(url)
        self.assertIn(response.status_code, [204, 200, 202])

class AnswerAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='auser', password='testpass')
        UserProfile.objects.create(user=self.user, role='USER')
        self.client.force_authenticate(user=self.user)
        self.question = Question.objects.create(title='Q', content='C', created_by=self.user, status='APPROVED')
        self.answer = Answer.objects.create(question=self.question, body='A', answered_by=self.user)

    def test_answer_list(self):
        url = reverse('question-answers-list', kwargs={'question_pk': self.question.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_answer_create(self):
        url = reverse('question-answers-list', kwargs={'question_pk': self.question.id})
        data = {'body': 'Another answer'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

class QuestionVoteAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='vuser', password='testpass')
        UserProfile.objects.create(user=self.user, role='USER')
        self.client.force_authenticate(user=self.user)
        self.question = Question.objects.create(title='Q', content='C', created_by=self.user, status='APPROVED')

    def test_vote_create(self):
        url = reverse('question-votes-list', kwargs={'question_pk': self.question.id})
        data = {'vote_type': 'LIKE'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

class ReportAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ruser', password='testpass', is_staff=True)
        UserProfile.objects.create(user=self.user, role='ADMIN')
        self.client.force_authenticate(user=self.user)
        self.question = Question.objects.create(title='Q', content='C', created_by=self.user)

    def test_report_create(self):
        url = reverse('reports-list')
        data = {'question': self.question.id, 'user': self.user.id, 'status': 'PENDING'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)