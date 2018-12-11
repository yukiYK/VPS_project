from django.db import models


# Create your models here.
class Authenticator(models.Model):
    name = models.CharField(max_length=20)
    number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    note = models.CharField(max_length=100)

    class Meta:
        db_table = 'authenticator'
