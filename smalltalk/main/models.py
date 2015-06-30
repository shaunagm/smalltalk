from django.db import models
from django.core.urlresolvers import reverse

class Contact(models.Model):
    name = models.CharField(max_length=100, unique=True)
    details = models.TextField(max_length=5000, blank=True)

    def get_url(self):
        return reverse('contact_detail', args=[self.pk])
