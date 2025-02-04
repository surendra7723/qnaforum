from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.response import Response
from .models import (
    Question, Answer, QuestionVote,
    AnswerVote,UserProfile,
    Report
    )
from .permissions import IsQuestionApprovedOrOwner,IsAdminOrReadOnly,IsOwnerOrAdmin
from .serializers import (
    QuestionSerializer, AnswerSerializer, 
    QuestionVoteSerializer, AnswerVoteSerializer,
    UserProfileSerializer,ReportSerializer
)
from .permissions import (
    IsOwnerOrAdmin,IsQuestionApprovedOrOwner,
    CanVoteOnQuestion,CanVoteOnAnswer,
)

# class UserSerializer()

class UserProfileViewset(CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,GenericViewSet):
    # permission_classes=[IsAuthenticated,IsOwnerOrAdmin]
    queryset=UserProfile.objects.all()
    serializer_class=UserProfileSerializer 
    
    # def get_queryset(self):
    #     req_user=self.request.user
        
    #     if req_user.is_authenticated and req_user.profile.role == "ADMIN":
    #         return UserProfile.objects.all()
    #     return UserProfile.objects.filter(user=req_user)
        
        
    
    def perform_create(self, serializer):
        serializer.save()
    

    


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrAdmin]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.profile.role == "ADMIN":
            return Question.objects.all()  
        return Question.objects.filter(Q(status="APPROVED") | Q(created_by=user))



class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer

    def get_queryset(self):
        question_id = self.kwargs["question_pk"] 
        # print(self.kwrgs)
         
        queryset = Answer.objects.filter(question__id=int(question_id))
        question = Question.objects.get(id = int(question_id))

        if question.status == "APPROVED" or self.request.user.profile.role=="ADMIN" :
            
            return queryset
         
        # elif self.request.user.profile.role=="ADMIN":
        #     return 
        
        else:
            raise PermissionDenied({"message":"Question is not approved yet to answer "})
        

class QuestionVoteViewSet(viewsets.ModelViewSet):
    permission_classes = [CanVoteOnQuestion,IsQuestionApprovedOrOwner]
    queryset=Question.objects.all()
    serializer_class = QuestionVoteSerializer
    

    # def get_queryset(self):
    #     question_id = self.kwargs["pk"]  
    #     return QuestionVote.objects.filter(question_id=question_id)  


class AnswerVoteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,CanVoteOnAnswer,IsQuestionApprovedOrOwner]
    queryset=AnswerVote.objects.all()
    serializer_class = AnswerVoteSerializer
    # def get_queryset(self):
    #     question_pk = self.kwargs["question_pk"]  
    #     answer_pk = self.kwargs["answer_pk"]  
    #     return AnswerVote.objects.filter(answer_id=answer_pk, answer__question_id=question_pk)  
    

class ReportViewset(viewsets.ModelViewSet):
    permission_classes=[IsOwnerOrAdmin,IsAuthenticated]
    queryset=Report.objects.all()
    
    
    serializer_class=ReportSerializer
    
    def get_queryset(self):
        user=self.request.user
        # print(type(user))
        if user.is_authenticated and user.profile.role=="ADMIN":
            return Report.objects.all()
        # return Report.objects.filter(Q())
        return Report.objects.filter(user=user)