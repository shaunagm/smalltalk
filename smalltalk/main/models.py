from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100, unique=True)
    details = models.TextField(max_length=5000, blank=True)

    def get_url(self):
        return "/fakecontacturl/"
#        return reverse('contact_detail', args=[self.pk])
