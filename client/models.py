from django.db import models
from django.contrib.auth.models import User
from lead.models import Lead


# Create your models here.
class Client(models.Model):
    resale = 'resale'
    direct = 'direct'

    CHOICES_STATUS = (
        (resale, 'Resale'),
        (direct, 'Direct'),
    )

    status = models.CharField(max_length=255, choices=CHOICES_STATUS, default='', blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    zipcode = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='clients', on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)
    converted_from_lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True, related_name="converted_client")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

class Comment(models.Model):
    client = models.ForeignKey(Client, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='client_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.username

class ClientFile(models.Model):
    client = models.ForeignKey(Client, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='clientfiles')
    created_by = models.ForeignKey(User, related_name='client_files', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.username
