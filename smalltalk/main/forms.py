from django.forms import ModelForm
from .models import Contact, Group

class ContactForm(ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'details']

class GroupForm(ModelForm):

    class Meta:
        model = Group
        fields = ['name', 'details']
