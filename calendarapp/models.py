from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.title
