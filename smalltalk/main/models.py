from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100, unique=True)
    details = models.TextField(max_length=5000, blank=True)
