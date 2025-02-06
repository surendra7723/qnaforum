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
        model=User
        # fields=['username']
        fields="__all__"

    def create(self, validated_data):
        username=validated_data['username']
        email=validated_data['email']
        password=validated_data['password']
        user_obj=User(username=username,email=email)
        user_obj.set_password(password)
        user_obj.save
        return user_obj
    
    
    def update(self, instance, validated_data):
        
            
        user = super().update(instance, validated_data)
        
            
            
        if 'password' in validated_data:
            # breakpoint()
            
            
                
            old_password = self.context['request'].data.get('old_password')  

            if old_password:
                    
                if not user.check_password(old_password):
                    raise serializers.ValidationError("Current password is incorrect.")
                
                
            user.set_password(validated_data['password'])
            user.save()

            return user
            

    
        
    
    

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
        
class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.HyperlinkedIdentityField(
        view_name='question-answers-list',  
        lookup_url_kwarg='question_pk'  
    )
    votes = serializers.HyperlinkedIdentityField(
        view_name='question-votes-list',  
        lookup_url_kwarg='question_pk'  
    )
    total_likes = serializers.ReadOnlyField()
    created_by = serializers.StringRelatedField(source="created_by.profile", read_only=True)
    download_report_url = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            "id", "title", "total_likes", "status", "content", "image", 
            "created_at", "remarks", "topic", "created_by", "url", 
            "answers", "votes", "download_report_url"
        ]
        read_only_fields = ["status"]

    def get_download_report_url(self, obj):
       
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
    
    def save(self, *args, **kwargs):
    
        existing_vote = QuestionVote.objects.filter(voter=self.voter, question=self.question).first()
        
        if existing_vote:
            
            existing_vote.vote_type = self.vote_type
            existing_vote.save()  
            return  

    
        super().save(*args, **kwargs)

    
class AnswerSerializer(serializers.ModelSerializer):
    
    
    class Meta:      
        model=Answer
        fields=["id","body","answered_at","edited"]
    
    def update(self, instance, validated_data):
        
        validated_data.pop("answered_by", None)  
        validated_data.pop("edited")
        validated_data["edited"]=True
        # breakpoint()

        
        return super().update(instance, validated_data)

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data.pop("edited")
        validated_data["edited"]=True
        if request and request.user.is_authenticated:
            validated_data["answered_by"] = request.user  # 
        return super().create(validated_data)


class QuestionVoteSerializer(serializers.ModelSerializer):
    voter_username = serializers.CharField(source="voter.username", read_only=True)
    voter = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # Auto-set voter

    class Meta:
        model = QuestionVote
        fields = ["id", "question", "voter", "voter_username", "vote_type", "created_at"]

    def validate(self, data):
        
        request = self.context.get("request")
        user = request.user
        question = data.get("question")

        if QuestionVote.objects.filter(voter=user, question=question).exists():
            raise serializers.ValidationError("You have already voted on this question.")

        return data
    
class AnswerVoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=AnswerVote
        fields="__all__"


class ReportSerializer(serializers.ModelSerializer):
    
    question_title=serializers.SerializerMethodField()
    
    
    
    
    
    class Meta:    
        model=Report
        fields="__all__"
        # read_only_fields=['User']
    
    answers = serializers.HyperlinkedIdentityField(
        view_name='question-answers-list',  
        lookup_url_kwarg='question_pk'  
    )
    votes = serializers.HyperlinkedIdentityField(
        view_name='question-votes-list',  
        lookup_url_kwarg='question_pk'  
    )
    
    def get_question_title(self,obj):
        return obj.question.title 
