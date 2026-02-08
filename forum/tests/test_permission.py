from django.test import TestCase
from forum.permissions import IsAdminOrReadOnly, IsOwnerOrAdmin, IsOwnerOrAdminForAnswer, IsAuthenticatedAndCanVote, CanGenerateOrViewReport
from rest_framework.test import APIRequestFactory
from forum.models import Question, UserProfile, Answer
from django.contrib.auth.models import User

class PermissionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='testpass')
        UserProfile.objects.create(user=self.user, role='USER')
        self.other_user = User.objects.create_user(username='other', password='testpass')
        UserProfile.objects.create(user=self.other_user, role='USER')
        self.question = Question.objects.create(title='Q', content='C', created_by=self.user)
        self.answer = Answer.objects.create(question=self.question, body='A', answered_by=self.user)
        self.factory = APIRequestFactory()

    def test_owner_permission(self):
        request = self.factory.get('/')
        request.user = self.user
        perm = IsOwnerOrAdmin()
        self.assertTrue(perm.has_object_permission(request, None, self.question))

    def test_admin_or_read_only_permission(self):
        request = self.factory.get('/')
        perm = IsAdminOrReadOnly()
        self.assertTrue(perm.has_permission(request, None))

        request = self.factory.post('/')
        request.user = self.user
        perm = IsAdminOrReadOnly()
        self.assertFalse(perm.has_permission(request, None))

        request.user = self.other_user
        self.assertFalse(perm.has_permission(request, None))

    def test_owner_or_admin_for_answer_permission(self):
        request = self.factory.get('/')
        request.user = self.user
        perm = IsOwnerOrAdminForAnswer()
        self.assertTrue(perm.has_object_permission(request, None, self.answer))

        request.user = self.other_user
        self.assertFalse(perm.has_object_permission(request, None, self.answer))

    def test_authenticated_and_can_vote_permission(self):
        request = self.factory.get('/')
        request.user = self.user
        perm = IsAuthenticatedAndCanVote()
        self.assertTrue(perm.has_permission(request, None))

        request.user = type('Anonymous', (), {'is_authenticated': False, 'is_staff': False})()
        self.assertFalse(perm.has_permission(request, None))

    def test_can_generate_or_view_report_permission(self):
        # Safe method (GET) should always allow
        request = self.factory.get('/')
        request.user = self.user
        perm = CanGenerateOrViewReport()
        self.assertTrue(perm.has_permission(request, None))

        # Unsafe method (POST) should only allow staff
        request = self.factory.post('/')
        request.user = self.user  # not staff
        self.assertFalse(perm.has_permission(request, None))

        request.user = self.other_user  # also not staff
        self.assertFalse(perm.has_permission(request, None))