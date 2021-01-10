from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.TextField(default=None, blank=True, null=True)
    father_name = models.CharField(max_length=50, default=False, null=True, blank=True)
    mother_name = models.CharField(max_length=50, default=False, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.user.username



