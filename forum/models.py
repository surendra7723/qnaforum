from django.db import models
from django.contrib.auth.models import User




#TODO :automatically create user profile when user is created if instance does not come from serializer 
#TODO :automatically  set user role to admin if the user is_staff

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("ADMIN", "Admin"),
        ("USER", "User"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="USER")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Use auto_now for updates

    def __str__(self):
        return f"{self.user.username} ({self.role})"
    

class Question(models.Model):
    STATUS_CHOICES=[
        ("PENDING","Pending"),
        ("APPROVED","Approved"),
        ("DENIED","Denied"),
    ]
    TOPIC_CHOICES=[
        ("GENERAL","General"),
        ("TECHNICAL","Technical"),
        ("FINANCE","Finance"),
        ("HR","Human Resouce"),
        ("FEEDBACK","Feedback"),
        ("SALES","Sales"),
        ("CUSTOMER",'Customer'),  
    ]
    
    title=models.CharField(max_length=60)
    content=models.TextField()
    image=models.ImageField(upload_to='images',blank=True,null=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=15,choices=STATUS_CHOICES,default="PENDING")
    remarks=models.TextField(null=True,blank=True)
    topic=models.CharField(choices=TOPIC_CHOICES,default="GENERAL",max_length=15)

    @property
    def total_likes(self):
        return self.q_votes.filter(vote_type="LIKE").count()
    
    @property
    def total_dislikes(self):
        return self.q_votes.filter(vote_type="DISLIKE").count()
    
    
    def __str__(self):
        return f"Question:{self.id}:{self.title} by {self.created_by}"
        

class Answer(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE,related_name='questionanswers')
    body=models.TextField()
    answered_at=models.DateTimeField(auto_now_add=True)
    answered_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='useranswers')
    edited=models.BooleanField(default=False)
    
    def __str__(self):
        return f" answer for {self.question} by {self.answered_by}"
    
    

class QuestionVote(models.Model):
    VOTE_CHOICES=[
        ("LIKE",'Like'),
        ("DISLIKE","Dislike"),
        
    ]
    question=models.ForeignKey(Question,on_delete=models.CASCADE,related_name='q_votes')
    voter=models.ForeignKey(User,on_delete=models.CASCADE,related_name="q_votes")
    vote_type=models.CharField(choices=VOTE_CHOICES,null=True,blank=True,max_length=10)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('voter','question')
    

    
    def __str__(self):
        return f"vote for {self.question.id} by {self.voter.username}"
    

    
        
        

class AnswerVote(models.Model):
    VOTE_CHOICES=[
        
        ("LIKE",'Like'),
        ("DISLIKE","Dislike"),
        ]
    
    answer=models.ForeignKey(Answer,on_delete=models.CASCADE,related_name='a_votes')
    voter=models.ForeignKey(User,on_delete=models.CASCADE,related_name='a_votes')
    vote_type=models.CharField(max_length=10,choices=VOTE_CHOICES,null=True,blank=True)
    create_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together=("answer",'voter')
        
    def __str__(self):
        return f"vote on answer {self.answer.id} by {self.voter.username}" 
    
        
        
class Report(models.Model):
    STATUS_CHOICES=[
        ("PENDING","Pending"),
        ("APPROVED","Approved"),
        ("REJECTED","Rejected"),
    ]
    question=models.ForeignKey(Question,on_delete=models.CASCADE,related_name='reports')
    feedback=models.TextField(null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reports')
    status=models.CharField(choices=STATUS_CHOICES,max_length=10,default="PENDING")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.status == "APPROVED":
            self.question.status = "APPROVED"
            self.question.save()

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Report on Question {self.question.id} for {self.user} "
    
    
    
    
        
    

        
   

    
    
    
    
    
    
    
    
         
    
    
    



# Create your models here.
