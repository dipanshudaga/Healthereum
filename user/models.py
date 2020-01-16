from django.db import models
from django.contrib.auth.models import User
from hospital.models import Hospital, City, State
from django.dispatch import receiver
from django.db.models.signals import post_save

GENDER = (
    ('M','Male'),
    ('F','Female'),
)

def user_profile_pic_path(instance, filename):
    return 'profile_pic/doc/{0}'.format(instance.user.username)

class Specialization(models.Model):
    field_name = models.CharField(max_length=15)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to=user_profile_pic_path, null=True, blank=True)
    contact = models.CharField(max_length=10)
    age = models.IntegerField()
    gender = models.CharField(choices=GENDER, max_length=1)
    email = models.CharField(max_length=20, blank=True, null=False)
    unique_id = models.CharField(max_length=20)
    address = models.TextField()
    pincode = models.CharField(max_length=6)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    skills = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    
    # @receiver(post_save, sender=User)
    # def create_doc_profile(sender, instance, created, **kwargs):
    #     if kwargs['isDoc'] is True:
    #         if created:
    #             Profile.objects.create(user=instance)
    #         else:
    #             instance.profile.save()

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=10)
    age = models.IntegerField()
    address = models.TextField()
    pincode = models.CharField(max_length=6)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=20)
    
    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if kwargs['isDoc'] is False:    
    #         if created:
    #             Profile.objects.create(user=instance)
    #         else:
    #             instance.profile.save()