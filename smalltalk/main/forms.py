from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Contact, Group

class ContactForm(forms.ModelForm):
    shortname = forms.CharField(error_messages={'required': 'The name field is required.'})

    class Meta:
        model = Contact
        fields = ['shortname', 'details']

class GroupForm(forms.ModelForm):
    shortname = forms.CharField(error_messages={'required': 'The name field is required.'})

    class Meta:
        model = Group
        fields = ['shortname', 'details']

class ManageGroupsForm(forms.ModelForm):
    groups = forms.ModelChoiceField(queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple, empty_label=None)

    class Meta:
        model = Contact
        fields = ['groups']

    def __init__(self, *args, **kwargs):
        contact = kwargs.pop('contact', 0)
        super(ManageGroupsForm, self).__init__(*args, **kwargs)
        self.fields['groups'].initial = [group.pk for group in contact.group_set.all()]
