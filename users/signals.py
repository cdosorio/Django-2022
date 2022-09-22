
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# Listeners
def createProfile(sender, instance, created, **kwargs):
   if created:
       user = instance
       profile = Profile.objects.create(
           user = user,
           username = user.username,
           email = user.email,
           name = user.first_name
       )    
    
@receiver(post_save, sender=Profile)
def profileUpdated(sender, instance, created, **kwargs):
    print('Profile saved')
    print('Instance:', instance)
    print('Created', created)
    
def deleteUser(sender, instance, created, **kwargs):
    print('Profile deleted. Deleting user...')
    user = instance.user
    user.delete()
        

post_save.connect(createProfile, sender=User)
# post_save.connect(profileUpdated, sender=Profile) replaced with decorator
post_delete.connect(deleteUser, sender=Profile)