from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Lead(models.Model):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    CHOICES_PRIORITY = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    )

    NEW = 'new'
    CONTACTED = 'contacted'
    WON = 'won'
    LOST = 'lost'

    CHOICES_STATUS = (
        (NEW, 'New'),
        (CONTACTED, 'Contacted'),
        (WON, 'Won'),
        (LOST, 'Lost'),
    )

    resale = 'resale'
    direct = 'direct'

    STATUS = (
        (resale, 'Resale'),
        (direct, 'Direct'),
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    status_sale = models.CharField(max_length=255, choices=STATUS, default='', blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    zipcode = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=255, choices=CHOICES_PRIORITY, default=MEDIUM)
    status = models.CharField(max_length=255, choices=CHOICES_STATUS, default=NEW)
    converted_to_client = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='leads', on_delete=models.CASCADE)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# Lead Files
class LeadFile(models.Model):
    lead = models.ForeignKey(Lead, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='leadfiles')
    created_by = models.ForeignKey(User, related_name='lead_files', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.username


# Lead Comment
class Comment(models.Model):
    lead = models.ForeignKey(Lead, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='lead_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.username
