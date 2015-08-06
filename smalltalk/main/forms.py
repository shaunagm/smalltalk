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

class ManageContactsForm(forms.Form):
    contacts = forms.ModelChoiceField(queryset=Contact.objects.all(),
        widget=forms.CheckboxSelectMultiple, empty_label=None)

    def __init__(self, *args, **kwargs):
        linked_object = kwargs.pop('linked_object', 0)
        super(ManageContactsForm, self).__init__(*args, **kwargs)
        self.fields['contacts'].initial = [contact.pk for contact in linked_object.contacts.all()]

class ManageGroupsForm(forms.Form):
    groups = forms.ModelChoiceField(queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple, empty_label=None)

    def __init__(self, *args, **kwargs):
        linked_object = kwargs.pop('linked_object', 0)
        super(ManageGroupsForm, self).__init__(*args, **kwargs)
        self.fields['groups'].initial = [group.pk for group in linked_object.group_set.all()]

class ManageTopicsForm(forms.Form):
    topics = forms.ModelChoiceField(queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple, empty_label=None)

    def __init__(self, *args, **kwargs):
        linked_object = kwargs.pop('linked_object', 0)
        super(ManageTopicsForm, self).__init__(*args, **kwargs)
        self.fields['topics'].queryset = Topic.objects.all()
        self.fields['topics'].initial = [topic.pk for topic in linked_object.topic_set.all()]
