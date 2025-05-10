from django.urls import path
from rest_framework_nested import routers
from .views import QuestionViewSet, AnswerViewSet, QuestionVoteViewSet, UserProfileViewset, ReportViewset, AdminDownloadQuestionReportView,UserViewset

router = routers.DefaultRouter()
router.register('userprofiles', UserProfileViewset, basename='userprofiles')
router.register('questions', QuestionViewSet)
router.register('reports', ReportViewset, basename='reports')
# router.register('user',UserViewset)

questions_router = routers.NestedDefaultRouter(router, 'questions', lookup='question')
questions_router.register('answers', AnswerViewSet, basename='question-answers')
questions_router.register('votes', QuestionVoteViewSet, basename='question-votes')


# 
answers_router = routers.NestedDefaultRouter(questions_router, 'answers', lookup='answer')


urlpatterns = [
    path("admin/questions/<int:question_id>/download-report/", AdminDownloadQuestionReportView.as_view(), name="admin-download-question-report"),
] + router.urls + questions_router.urls + answers_router.urls
