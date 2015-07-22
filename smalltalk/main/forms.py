from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Contact, Group, Topic

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

class TopicForm(forms.ModelForm):
    shortname = forms.CharField(error_messages={'required': 'The name field is required.'})

    class Meta:
        model = Topic
        fields = ['shortname', 'details', 'link']

class ManageContactsForm(forms.ModelForm):
    contacts = forms.ModelChoiceField(queryset=Contact.objects.all(),
        widget=forms.CheckboxSelectMultiple, empty_label=None)

    class Meta:
        model = Group
        fields = ['contacts']

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', 0)
        super(ManageContactsForm, self).__init__(*args, **kwargs)
        self.fields['contacts'].initial = [contact.pk for contact in group.contacts.all()]

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
