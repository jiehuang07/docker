from django.db import models


# Create your models here.
class Provider(models.Model):
    providerID = models.TextField()
    providerName = models.TextField()
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "provider"
