from django.urls import path,include
from rest_framework_nested import routers
from .views import QuestionViewSet, AnswerViewSet, AnswerVoteViewSet, UserProfileViewset,ReportViewset


router = routers.DefaultRouter()

router.register('questions', QuestionViewSet)
router.register('userprofiles', UserProfileViewset, basename='userprofiles')
# router.register('profile',)

router.register('reports',ReportViewset,basename='reports')
questions_router = routers.NestedDefaultRouter(router, 'questions', lookup='question')

questions_router.register('answers', AnswerViewSet, basename='question-answers')
answers_router = routers.NestedDefaultRouter(questions_router, 'answers', lookup='answer')
answers_router.register('votes', AnswerVoteViewSet, basename='answer-votes')
# authurls=[
#     path('auth/',include('djoser.urls')),
 
# ]

urlpatterns = router.urls + questions_router.urls + answers_router.urls
