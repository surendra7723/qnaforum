from django.test import TestCase
from forum.permissions import IsOwnerOrAdmin
from rest_framework.test import APIRequestFactory
from forum.models import Question, UserProfile
from django.contrib.auth.models import User

class PermissionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='testpass')
        UserProfile.objects.create(user=self.user, role='USER')
        self.other_user = User.objects.create_user(username='other', password='testpass')
        UserProfile.objects.create(user=self.other_user, role='USER')
        self.question = Question.objects.create(title='Q', content='C', created_by=self.user)
        self.factory = APIRequestFactory()

    def test_owner_permission(self):
        request = self.factory.get('/')
        request.user = self.user
        perm = IsOwnerOrAdmin()
        self.assertTrue(perm.has_object_permission(request, None, self.question))