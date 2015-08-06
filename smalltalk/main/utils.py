import copy

from .models import Contact, Group, Topic, TopicContactRelationship, TopicGroupRelationship
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

def local_toggle(object_to_adjust, toggle_type):
    if toggle_type == "star":
        object_to_adjust.starred = not object_to_adjust.starred
    if toggle_type == "archive":
        object_to_adjust.archived = not object_to_adjust.archived
    object_to_adjust.save()
    return object_to_adjust

def global_toggle(object_to_adjust, toggle_type):
    original_object = copy.copy(object_to_adjust) # Save a separate copy for reference/use later
    if hasattr(object_to_adjust, 'topic'): # If this is a relationship object
        local_toggle(object_to_adjust, toggle_type) # Toggle the actual object
        object_to_adjust = object_to_adjust.topic # Replace with linked topic object
    if toggle_type == "star":
        star_status = False if original_object.starred else True
        object_to_adjust.starred = star_status
        TopicContactRelationship.objects.filter(topic__pk=object_to_adjust.pk).update(starred=star_status)
        TopicGroupRelationship.objects.filter(topic__pk=object_to_adjust.pk).update(starred=star_status)
    if toggle_type == "archive":
        archive_status = False if original_object.archived else True
        object_to_adjust.archived = archive_status
        TopicContactRelationship.objects.filter(topic__pk=object_to_adjust.pk).update(archived=archive_status)
        TopicGroupRelationship.objects.filter(topic__pk=object_to_adjust.pk).update(archived=archive_status)
    object_to_adjust.save()
    return object_to_adjust
