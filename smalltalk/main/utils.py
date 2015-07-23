from .models import Contact, Group, Topic
from .forms import (ContactForm, GroupForm, TopicForm, ManageContactsForm,
    ManageGroupsForm, ManageTopicsForm)

def contact_form_helper(linked_object):
    context = {}
    if Contact.objects.all():
        context['manage_contact_form'] = ManageContactsForm(linked_object=linked_object)
        if not linked_object.contacts.all():
            context['no_contacts_message'] = "You have not added any contacts yet."
    else:
        context['no_contacts_message'] = "You do not have any contacts to add.  Why don't you" \
            " try <a href='/contact/new/'>creating some</a>?"
    return context

def group_form_helper(linked_object):
    context = {}
    if Group.objects.all():
        context['manage_group_form'] = ManageGroupsForm(linked_object=linked_object)
        if not linked_object.group_set.all():
            context['no_groups_message'] = "You have not added any groups yet."
    else:
        context['no_groups_message'] = "You do not have any groups to add.  Why don't you" \
            " try <a href='/group/new/'>adding some</a>?"
    return context

def topic_form_helper(linked_object):
    context = {}
    if Topic.objects.all():
        context['manage_topic_form'] = ManageTopicsForm(linked_object=linked_object)
        if not linked_object.topic_set.all():
            context['no_topics_message'] = "You have not added any topics yet."
    else:
        context['no_topics_message'] = "You do not have any topics to add.  Why don't you" \
            " try <a href='/topic/new/'>adding some</a>?"
    return context
