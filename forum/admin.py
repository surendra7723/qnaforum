from django.contrib import admin
from .models import UserProfile, Question, Answer, QuestionVote, AnswerVote, Report


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'created_at', 'updated_at']
    search_fields = ['user__username']
    list_filter = ['role']
    readonly_fields = ['created_at', 'updated_at']  # Fields that shouldn't be edited


# class DiscussionTopicAdmin(admin.ModelAdmin):
#     list_display = ['name', 'created_by']
#     search_fields = ['name', 'created_by__username']
#     list_filter = ['name']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'created_by', 'created_at', 'status', 'total_likes', 'total_dislikes']
    search_fields = ['title', 'created_by__username']
    list_filter = ['status']  
    readonly_fields = ['created_at']  

    def total_likes(self, obj):
        return obj.total_likes
    total_likes.admin_order_field = 'total_likes'  

    def total_dislikes(self, obj):
        return obj.total_dislikes
    total_dislikes.admin_order_field = 'total_dislikes'  


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id','question__title','body', 'answered_by', 'answered_at']
    search_fields = ['question__title', 'answered_by__username']
    list_filter = ['answered_by']
    readonly_fields = ['answered_at']


class QuestionVoteAdmin(admin.ModelAdmin):
    list_display = ['question', 'voter', 'vote_type', 'created_at']
    search_fields = ['question__title', 'voter__username']
    list_filter = ['vote_type', 'created_at']
    readonly_fields = ['created_at']


class AnswerVoteAdmin(admin.ModelAdmin):
    list_display = ['answer', 'voter', 'vote_type', 'create_at']
    search_fields = ['answer__body', 'voter__username']
    list_filter = ['vote_type', 'create_at']
    readonly_fields = ['create_at']


class ReportAdmin(admin.ModelAdmin):
    list_display = ['question', 'status', 'user', 'created_at', 'updated_at']
    search_fields = ['question__title', 'user__username']
    list_filter = ['status', 'created_at']
    readonly_fields = ['created_at', 'updated_at']

  
    actions = ['approve_reports', 'reject_reports']

    def approve_reports(self, request, queryset):
        queryset.update(status='APPROVED')
        self.message_user(request, "Reports approved successfully")

    def reject_reports(self, request, queryset):
        queryset.update(status='REJECTED')
        self.message_user(request, "Reports rejected successfully")


admin.site.register(UserProfile, UserProfileAdmin)
# admin.site.register(DiscussionTopic, DiscussionTopicAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(QuestionVote, QuestionVoteAdmin)
admin.site.register(AnswerVote, AnswerVoteAdmin)
admin.site.register(Report, ReportAdmin)
