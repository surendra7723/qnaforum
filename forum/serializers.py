from rest_framework import serializers
# from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
# from rest_framework 
from .models import Question,Answer,UserProfile,QuestionVote,AnswerVote,Report
from django.contrib.auth.models import User



    

class UserProfileSerializer(serializers.ModelSerializer):
    username=serializers.SerializerMethodField()
    
    class Meta:
        model=UserProfile
        
        fields=['id','user_id','role','username']
    
    def get_username(self,obj):
        return obj.user.username
        
        
        
    # user=BaseUserCreateSerializer()
    # print(self.context)
    # print("hi")
    # user=UserCreateSerializer()
    # role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, default="USER")
    

    # class Meta:
    #     model = UserProfile 
        
    #     fields = ['role','user']


    # def create(self, validated_data):
    #     request=self.context.get('request')
        
    #     print(self.context)
        
    #     return User.objects.create(**validated_data)
            
        
        # role = validated_data.pop('role', 'USER')
        
        
        # user = User.objects.create_user(
        #     username=validated_data['username'],
        #     email=validated_data['email'],
        #     password=validated_data['password']
        # )


        # user_profile = UserProfile.objects.create(
        #     user=user,
        #     role=role
        # )

        # return user_profile
        
class QuestionSerializer(serializers.ModelSerializer):
    total_likes = serializers.ReadOnlyField()
    # def get_queryset(self):
    #     user = self.request.user

    created_by = serializers.StringRelatedField(source="created_by.profile", read_only=True)
    

    class Meta:
        model = Question
        fields = ["id","title","total_likes","status","content", "image", "created_at", "remarks", "topic","created_by"]
        
        
        read_only_fields=["status"]
        
    def validate_status(self, value): 
        request = self.context.get("request")
        if request and not request.user.is_staff:  
            print(request)
            raise serializers.ValidationError("You are not allowed to modify the status field.")
        return value
    

    
class AnswerSerializer(serializers.ModelSerializer):
    body = serializers.ReadOnlyField(allow_null=True)
    
    class Meta:      
        model=Answer
        fields=["id","body","answered_at","answered_by"]
    
    
    def perform_create(self, serializer):
        question_id = self.kwargs["question_pk"]
        serializer.save(created_by=self.request.user, question_id=question_id)

class QuestionVoteSerializer(serializers.ModelSerializer):
    voter_username=serializers.CharField(source="voter.username",read_only=True)
    
    
    class Meta:
        model=QuestionVote
        fields= ["id", "question", "voter", "voter_username", "vote_type", "created_at"]
    
    
class AnswerVoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=AnswerVote
        fields="__all__"


class ReportSerializer(serializers.ModelSerializer):
    # question=serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    
    class Meta:    
        model=Report
        fields="__all__"
        # fields=['status','question',]