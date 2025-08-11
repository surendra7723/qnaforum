# # signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile,Report,Question

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

@receiver(post_save, sender=Question)
def create_report(sender, instance, created, **kwargs):
    if created:
        if instance.created_by: 
            # print("hi INSIDE AFASFA")
            Report.objects.create(question=instance, user=instance.created_by)
        else:
            Report.objects.create(question=instance, user=User.objects.filter(is_superuser=True).first())

# @receiver(post_save, sender=UserProfile)
# def update_user_is_staff(sender, instance, **kwargs):
#     # Ensure superusers are not affected
#     if not instance.user.is_superuser:
#         instance.user.is_staff = instance.role == "ADMIN"
#         instance.user.save(update_fields=["is_staff"])


