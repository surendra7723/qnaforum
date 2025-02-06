from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.decorators import action

from openpyxl.styles import Font  
import openpyxl
from rest_framework import viewsets 
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import (
    Question, Answer, QuestionVote,
    AnswerVote,UserProfile,
    Report
    )
# from .permissions import IsAdminOrReadOnly,IsOwnerOrAdmin
from .serializers import (
    QuestionSerializer, AnswerSerializer, 
    QuestionVoteSerializer, AnswerVoteSerializer,
    ReportSerializer,
    UserSerializer,UserProfileSerializer
)
from .permissions import (
    IsOwnerOrAdmin,IsOwnerOrAdminForAnswer,IsAuthenticatedAndCanVote,CanGenerateOrViewReport
)



class UserProfileViewset(viewsets.ModelViewSet):
    permission_classes=[IsAdminUser]
    queryset=UserProfile.objects.all()
    serializer_class=UserProfileSerializer

    # # breakpoint()
    # serializer_class=UserProfileSerializer 
    
    
    def get_queryset(self):
        user=self.request.user
        
        if user.is_authenticated and user.profile.role == "ADMIN":
            return UserProfile.objects.all()
        # breakpoint()
        # print("kjdfhaksdfdsjfjas")
        return UserProfile.objects.get(id=user.id)
        
        
    
    # def perform_create(self, serializer):
    #     serializer.save()
    

    


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsOwnerOrAdmin]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
    
    @action(detail=True, methods=['get'], permission_classes=[IsAdminUser], url_path='download-report')
    def download_report(self, request, pk=None):
        
        try:
            question = Question.objects.get(id=pk)
        except Question.DoesNotExist:
            return Response({"error": "Question not found."}, status=404)

        
        answers = Answer.objects.filter(question=question)

        
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f"Question {pk}"

        
        question_cell = ws.cell(row=1, column=1, value=f"Question: {question.title}")
        question_cell.font = Font(bold=True)

        
        ws.append([])

        
        ws.append(["Answer ID", "Answer Text", "Answered By", "Created At"])

        
        for answer in answers:
            ws.append([
                answer.id,
                answer.body,
                answer.answered_by.username,
                answer.answered_at.strftime("%Y-%m-%d %H:%M:%S")
            ])

        
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="question_{question.id}_report.xlsx"'

        
        wb.save(response)

        return response

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:  
            raise PermissionDenied({"message": "Please Login First!"})

        if user.profile.role == "ADMIN":
            return Question.objects.all()
        elif user.profile.role == "USER":
            return Question.objects.filter(Q(status="APPROVED") | Q(created_by=user)).order_by('-created_at')

        return Question.objects.none()

class AdminDownloadQuestionReportView(APIView):
    permission_classes = [IsAdminUser]  

    def get(self, request, question_id):

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({"error": "Question not found."}, status=404)

        
        answers = Answer.objects.filter(question=question)

        
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f"Question {question_id}"

        
        question_cell = ws.cell(row=1, column=1, value=f"Question: {question.text}")
        question_cell.font = Font(bold=True)

        
        ws.append([])

        
        ws.append(["Answer ID", "Answer Text", "Answered By", "Created At"])

        
        for answer in answers:
            ws.append([
                answer.id,
                answer.text,
                answer.user.username,
                answer.created_at.strftime("%Y-%m-%d %H:%M:%S")
            ])

        
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="question_{question.id}_report.xlsx"'

        
        wb.save(response)

        return response
            



class AnswerViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class = AnswerSerializer

    def get_queryset(self):
        question_id = self.kwargs["question_pk"] 
        # breakpoint()
        # print(self.kwrgs)
        # if Question.objects.get(id=question_id):
             
        if Question.objects.get(id=question_id):
            queryset = Answer.objects.filter(question__id=int(question_id))
        else:
            raise {"message":"No Questin matching the query "}
    
        


        question = Question.objects.get(id = int(question_id))

        if question.status == "APPROVED" or self.request.user.profile.role=="ADMIN" :
            return queryset
        else:
            raise PermissionDenied({"message":"Question is not approved yet to answer "})
    
    def perform_create(self, serializer):
        question_id = self.kwargs.get("question_pk")
        serializer.save(question_id=question_id, answered_by=self.request.user)
        

class QuestionVoteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedAndCanVote]
    queryset=QuestionVote.objects.all()
    serializer_class = QuestionVoteSerializer
    
    def get_queryset(self):
        user=self.request.user

        
        question = get_object_or_404(Question, id=self.kwargs["question_pk"])
        
        votes= question.q_votes.all()
        
        if not question.status=="APPROVED":
            raise PermissionDenied({"message":"question is not approved yet to vote"})
        
        # elif question.status=="APPROVED":
            
            
            
        # elif not votes.exists():
        #     raise PermissionDenied({"message": "No votes till date"})
        

        return votes
        # queryset=QuestionVote.objects.filter(question__id=int(question_id))
        
        
        # return queryset
    

    # def get_queryset(self):
    #     question_id = self.kwargs["pk"]  
    #     return QuestionVote.objects.filter(question_id=question_id)  


class AnswerVoteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedAndCanVote]
    queryset=AnswerVote.objects.all()
    serializer_class = AnswerVoteSerializer
    # def get_queryset(self):
    #     question_pk = self.kwargs["question_pk"]  
    #     answer_pk = self.kwargs["answer_pk"]  
    #     return AnswerVote.objects.filter(answer_id=answer_pk, answer__question_id=question_pk)  
    

class ReportViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated,CanGenerateOrViewReport,IsOwnerOrAdmin]
    queryset=Report.objects.all()
    
    
    serializer_class=ReportSerializer
    
    def get_queryset(self):
        requester=(self.request.user)
        # breakpoint()
        # req_id=requester.id
        # breakpoint()
        # breakpoint()
        # print(type(user))
        if requester.profile.role=="ADMIN":
            # return Report.objects.filter(status="PENDING").order_by("-created_at")
            return Report.objects.all()
        
        return Report.objects.filter(user=requester).order_by("-created_at")


class UserViewset(viewsets.ModelViewSet):
    
    queryset=User.objects.all()
    serializer_class=UserSerializer
    
    def get_queryset(self):
        user=self.request.user
        if user.is_staff:
            return User.objects.all()
        elif not user.is_staff:
            return User.objects.filter(id=user.id)
            
            
            
        
    