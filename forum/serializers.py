from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from .models import QuestionVote
from .models import Question, Answer, UserProfile, QuestionVote, AnswerVote, Report
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import transaction

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    oldpassword = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "oldpassword"]
        extra_kwargs = {
            "password": {"write_only": True},
            "oldpassword": {"write_only": True},
        }
    def to_representation(self, instance):
        # Exclude 'oldpassword' from output
        ret = super().to_representation(instance)
        ret.pop('oldpassword', None)
        return ret



    def validate_password(self, value):
        # Add custom password validation logic here
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            is_active=True  # Ensure the user is active by default
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        old_password = validated_data.pop("oldpassword", None)
        if "password" in validated_data:
            if not old_password or not instance.check_password(old_password):
                raise serializers.ValidationError({"oldpassword": "Current password is incorrect."})
            instance.set_password(validated_data["password"])
        # Prevent updating sensitive fields
        validated_data.pop("is_superuser", None)
        validated_data.pop("is_staff", None)
        return super().update(instance, validated_data)
    

class CustomUserCreateSerializer(BaseUserCreateSerializer):
    class Meta:
        model=BaseUserCreateSerializer.Meta.model
        fields=BaseUserCreateSerializer.Meta.fields
        
    def perform_create(self,validated_data):
        with transaction.atomic():
            user=super().perform_create(validated_data)
            UserProfile.objects.create(
                user=user,
                role="USER"
            )
            return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "role","profile_pic",'favicon']
        
    def create(self,validated_data):
        profile=UserProfile.objects.create(**validated_data)

        if profile.profile_pic:
            profile.process_profile_image()
        
        return profile


class UserProfileThinSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id","favicon","role"]
        read_only_fields=fields

class AnswerSerializer(serializers.ModelSerializer):
    answered_by = serializers.SlugRelatedField(slug_field="username", read_only=True)
    question_title = serializers.CharField(source='question.title', read_only=True)
    question = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = ["id", "question", "question_title", "body", "answered_at", "edited", "answered_by"]
        read_only_fields = ["edited", "question"]

#TODO:fetch some more detail in user not just slug of user like name, profile(favicon-small), department,
class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    votes = serializers.HyperlinkedIdentityField(
        view_name='question-votes-list',
        lookup_url_kwarg='question_pk'
    )
    created_by = serializers.SlugRelatedField(slug_field="username", read_only=True)
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

    def get_answers(self, obj):
        return obj.questionanswers.all().values("body", "answered_by", "answered_at")

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

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user
        return super().create(validated_data)


class QuestionVoteSerializer(serializers.ModelSerializer):
    voter_username = serializers.CharField(source="voter.username", read_only=True)
    voter = serializers.HiddenField(default=serializers.CurrentUserDefault())
    question = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = QuestionVote
        fields = ["id", "question", "voter", "voter_username", "vote_type", "created_at"]
        read_only_fields = ["question"]

    def validate(self, data):
        user = self.context["request"].user
        question = self.instance.question if self.instance else self.context.get('question')
        if not question:
            question = data.get("question")
        existing_vote = QuestionVote.objects.filter(voter=user, question=question).first()

        if existing_vote:
            if existing_vote.vote_type == data["vote_type"]:
                raise serializers.ValidationError("You have already cast this vote.")
            existing_vote.vote_type = data["vote_type"]
            existing_vote.save()
            return existing_vote

        return data


class AnswerVoteSerializer(serializers.ModelSerializer):
    voter = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = AnswerVote
        fields = ["id", "answer", "voter", "vote_type", "create_at"]


class ReportSerializer(serializers.ModelSerializer):
    question_title = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = "__all__"

    def get_question_title(self, obj):
        return obj.question.title
