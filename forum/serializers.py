from rest_framework import serializers
from .models import QuestionVote
from rest_framework import serializers
# from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
# from rest_framework 
from .models import Question,Answer,UserProfile,QuestionVote,AnswerVote,Report
from django.contrib.auth.models import User
from django.urls import reverse



class UserSerializer(serializers.ModelSerializer):
    
    
    username=serializers.SerializerMethodField()
    oldpassword=serializers.CharField()
    class Meta:
            model = User
            fields = ["id", "username", "email", "password", "old_password"]

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        old_password = validated_data.pop("old_password", None)

        if "password" in validated_data:
            if not old_password or not instance.check_password(old_password):
                raise serializers.ValidationError({"old_password": "Current password is incorrect."})
            instance.set_password(validated_data["password"])

        return super().update(instance, validated_data)
    
    
   
    
        
    
    

class UserProfileSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model=UserProfile
        
        fields=["id",'role',]  
    
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
class AnswerSerializer(serializers.ModelSerializer):
    answered_by = serializers.SlugRelatedField(slug_field="username", read_only=True)
    question_title = serializers.CharField(source='question.title', read_only=True)

    class Meta:
        model = Answer
        fields = ["id", "question","question_title","body", "answered_at", "edited", "answered_by"]
        read_only_fields=["edited"]
        
class QuestionSerializer(serializers.ModelSerializer):
    # answers = serializers.HyperlinkedIdentityField(
    #     view_name='question-answers-list',  
    #     lookup_url_kwarg='question_pk'  
    # )
    answers=serializers.SerializerMethodField('get_answers')
    
    votes = serializers.HyperlinkedIdentityField(
        view_name='question-votes-list',  
        lookup_url_kwarg='question_pk'  
    )
    created_by = serializers.SlugRelatedField(slug_field="username",read_only=True)
    total_likes = serializers.ReadOnlyField()
    download_report_url = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            "id", "title", "total_likes", "status", "content", "image", 
            "created_at", "remarks", "topic", "created_by", "url", 
            "answers", "votes", "download_report_url"
        ]
        read_only_fields = ["status"]
        
    def get_answers(self,obj):
        return obj.questionanswers.all().values("body","answered_by","answered_at")

    def get_download_report_url(self, obj):
       
        # breakpoint()
        request = self.context.get("request")
        if request and request.user.is_staff:
            return request.build_absolute_uri(
                reverse('question-download-report', kwargs={'pk': obj.id})
                
            )
        return None  

    def validate_status(self, value): 
        request = self.context.get("request")
        if request and not request.user.is_staff:  
            raise serializers.ValidationError("You are not allowed to modify the status field.")
        return value
    


    

    def update(self, instance, validated_data):
        if "body" in validated_data:
            validated_data["edited"] = True
        return super().update(instance, validated_data)

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user
        return super().create(validated_data)


class QuestionVoteSerializer(serializers.ModelSerializer):
    voter_username = serializers.CharField(source="voter.username", read_only=True)
    voter = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # Auto-set voter

    class Meta:
        model = QuestionVote
        fields = ["id", "question", "voter", "voter_username", "vote_type", "created_at"]

    def validate(self, data):
        user = self.context["request"].user
        question = data["question"]
        existing_vote = QuestionVote.objects.filter(voter=user, question=question).first()

        if existing_vote:
            if existing_vote.vote_type == data["vote_type"]:
                raise serializers.ValidationError("You have already cast this vote.")
            existing_vote.vote_type = data["vote_type"]
            existing_vote.save()
            raise serializers.ValidationError("Vote updated.")

        return data
    
class AnswerVoteSerializer(serializers.ModelSerializer):
    voter = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = AnswerVote
        fields = ["id", "answer", "voter", "vote_type", "created_at"]


class ReportSerializer(serializers.ModelSerializer):
    
    question_title=serializers.SerializerMethodField()
    
    
    
    
    
    class Meta:    
        model=Report
        fields="__all__"
        # read_only_fields=['User']
    
    # answers = serializers.HyperlinkedIdentityField(
    #     view_name='question-answers-list',  
    #     lookup_url_kwarg='question_pk'  
    # )
    # votes = serializers.HyperlinkedIdentityField(
    #     view_name='question-votes-list',  
    #     lookup_url_kwarg='question_pk'  
    # )
    
    def get_question_title(self,obj):
        return obj.question.title 
