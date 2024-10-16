from django.db import models
from django.contrib.auth.models import User

class Community(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    purpose = models.TextField()
    mission = models.TextField()
    vision = models.TextField()
    # admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def str(self):
        return self.name
    
# class User(models.Model):
#     name = models.CharField(max_length=50)
#     email = models.EmailField()
#     password = models.CharField(max_length=20)
#     Community = models.ForeignKey(Community, on_delete= models.CASCADE) 

#     def str(self):
#         return self.name   

class CommunityAdmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username   

class ElectionOfficer(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='election_officers')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def str(self):
        return self.user.username