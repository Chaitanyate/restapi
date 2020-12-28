from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class post(models.Model):
    title=models.CharField(max_length=100)
    url=models.URLField()
    poster=models.ForeignKey(User,on_delete=models.CASCADE)

    class meta:
        ordering=['-created']

class vote(models.Model):
    voter=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(post,on_delete=models.CASCADE)

