from django.forms import ModelForm, CharField
from django.utils.translation import ugettext_lazy as _

from .models import Contact, Group

class ContactForm(ModelForm):
    name = CharField(error_messages={'required': 'The name field is required.'})

    class Meta:
        model = Contact
        fields = ['name', 'details']

class GroupForm(ModelForm):

    class Meta:
        model = Group
        fields = ['name', 'details']
