import unittest
import json

from django.core.urlresolvers import resolve
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from .models import Contact, Group, Topic, TopicContactRelationship, TopicGroupRelationship
from .utils import (group_form_helper, contact_form_helper, topic_form_helper, global_toggle,
    local_toggle)

###############################
### Model Method Unit Tests ###
###############################

class TestContactModel(TestCase):

    fixtures = ['test_fixtures']

    def setUp(self):
        self.contact_object = Contact.objects.create(shortname="Dawn")

    def test_contact_url(self):
        self.assertEqual("/contact/10/",
            self.contact_object.get_url())

    def test_get_group_pks(self):
        self.assertEqual(0,
            len(self.contact_object.get_group_pks()))
        self.contact_object.group_set.add(Group.objects.get(pk=4))
        self.assertEqual(1,
            len(self.contact_object.get_group_pks()))
        self.contact_object.group_set.remove(Group.objects.get(pk=4))
        self.assertEqual(0,
            len(self.contact_object.get_group_pks()))

    def test_get_topic_pks(self):
        self.assertEqual(0,
            len(self.contact_object.get_topic_pks()))
        relationship = TopicContactRelationship.objects.create(topic_id=1,
            contact=self.contact_object)
        self.assertEqual(1,
            len(self.contact_object.get_topic_pks()))
        # Archive the relationship and test that get_topic_pks returns it
        relationship.archived = 1
        relationship.save()
        self.assertEqual(1,
            len(self.contact_object.get_topic_pks()))

    def test_adjust_group_by_adding_groups(self):
        self.contact_object.adjust_groups(set([4,5,6]))
        self.assertEqual(3,
            len(self.contact_object.group_set.all()))
        self.assertEqual(['People', 'Scoobies', 'Vampires'],
            [group.shortname for group in self.contact_object.group_set.all()])

    def test_adjust_group_by_removing_groups(self):
        self.contact_object.group_set.add(Group.objects.get(pk=4))
        self.contact_object.group_set.add(Group.objects.get(pk=5))
        self.assertEqual(2,
            len(self.contact_object.group_set.all()))
        self.contact_object.adjust_groups(set([5]))
        self.assertEqual(1,
            len(self.contact_object.group_set.all()))
        self.assertEqual(['Scoobies'],
            [group.shortname for group in self.contact_object.group_set.all()])

    def test_adjust_topics_by_adding_topics(self):
        self.contact_object.adjust_topics(set([1,2,3]))
        self.assertEqual(3,
            len(self.contact_object.topics.all()))
        self.assertEqual(['Apocalypse', 'The Bronze', 'Stakes'],
            [topic.topic.shortname for topic in self.contact_object.topics.all()])

    def test_adjust_topics_by_removing_topics(self):
        TopicContactRelationship.objects.create(contact=self.contact_object,
            topic_id=1)
        TopicContactRelationship.objects.create(contact=self.contact_object,
            topic_id=2)
        self.assertEqual(2,
            len(self.contact_object.topics.all()))
        self.contact_object.adjust_topics(set([1]))
        self.assertEqual(1,
            len(self.contact_object.topics.all()))
        self.assertEqual(['Apocalypse'],
            [topic.topic.shortname for topic in self.contact_object.topics.all()])

class TestGroupModel(TestCase):

    fixtures = ['test_fixtures']

    def setUp(self):
        self.group_object = Group.objects.create(shortname="Ladies")

    def test_group_url(self):
        self.assertEqual("/group/7/",
            self.group_object.get_url())

    def test_get_contact_pks(self):
        self.assertEqual(0,
            len(self.group_object.get_contact_pks()))
        self.group_object.contacts.add(Contact.objects.get(pk=9))
        self.assertEqual(1,
            len(self.group_object.get_contact_pks()))
        self.group_object.contacts.remove(Contact.objects.get(pk=9))
        self.assertEqual(0,
            len(self.group_object.get_contact_pks()))

    def test_get_topic_pks(self):
        self.assertEqual(0,
            len(self.group_object.get_topic_pks()))
        relationship = TopicGroupRelationship.objects.create(topic_id=1,
            group=self.group_object)
        self.assertEqual(1,
            len(self.group_object.get_topic_pks()))
        # Archive the relationship and test that get_topic_pks returns it
        relationship.archived = 1
        relationship.save()
        self.assertEqual(1,
            len(self.group_object.get_topic_pks()))

    def test_adjust_contact_by_adding_contacts(self):
        self.group_object.adjust_contacts(set([2,3,4]))
        self.assertEqual(3,
            len(self.group_object.contacts.all()))
        self.assertEqual(['Giles', 'Snyder', 'Spike'],
            [contact.shortname for contact in self.group_object.contacts.all()])

    def test_adjust_contact_by_removing_contacts(self):
        self.group_object.contacts.add(Contact.objects.get(pk=2))
        self.group_object.contacts.add(Contact.objects.get(pk=3))
        self.assertEqual(2,
            len(self.group_object.contacts.all()))
        self.group_object.adjust_contacts(set([3]))
        self.assertEqual(1,
            len(self.group_object.contacts.all()))
        self.assertEqual(['Giles'],
            [contact.shortname for contact in self.group_object.contacts.all()])

    def test_adjust_topics_by_adding_topics(self):
        self.group_object.adjust_topics(set([1,2,3]))
        self.assertEqual(3,
            len(self.group_object.topics.all()))
        self.assertEqual(['Apocalypse', 'The Bronze', 'Stakes'],
            [topic.topic.shortname for topic in self.group_object.topics.all()])

    def test_adjust_topics_by_removing_topics(self):
        TopicGroupRelationship.objects.create(group=self.group_object,
            topic_id=1)
        TopicGroupRelationship.objects.create(group=self.group_object,
            topic_id=2)
        self.assertEqual(2,
            len(self.group_object.topics.all()))
        self.group_object.adjust_topics(set([1]))
        self.assertEqual(1,
            len(self.group_object.topics.all()))
        self.assertEqual(['Apocalypse'],
            [topic.topic.shortname for topic in self.group_object.topics.all()])

    def test_add_new_topic_to_contact_via_group(self):
        self.group_object.add_topic_to_contact(topic=Topic.objects.get(pk=2),
            contact=Contact.objects.get(pk=5))
        self.assertEqual("Ladies",
            TopicContactRelationship.objects.get(topic_id=2, contact_id=5).via_group_name.shortname)

    def test_add_existing_topic_to_contact_via_group(self):
        self.group_object.add_topic_to_contact(topic=Topic.objects.get(pk=2),
            contact=Contact.objects.get(pk=9))
        self.assertEqual(None,
            TopicContactRelationship.objects.get(topic_id=2, contact_id=9).via_group_name)

    def test_remove_topic_from_contact_via_unrelated_group(self):
        self.assertEqual(1,
            len(TopicContactRelationship.objects.filter(topic_id=2, contact_id=9)))
        # Won't remove because contact wasn't made via group & override isn't passed.
        self.group_object.remove_topic_from_contact(topic=Topic.objects.get(pk=2),
            contact=Contact.objects.get(pk=9))
        self.assertEqual(1,
            len(TopicContactRelationship.objects.filter(topic_id=2, contact_id=9)))
        # Now will remove contact!
        self.group_object.remove_topic_from_contact(topic=Topic.objects.get(pk=2),
            contact=Contact.objects.get(pk=9), override=True)
        self.assertEqual(0,
            len(TopicContactRelationship.objects.filter(topic_id=2, contact_id=9)))

    def test_remove_topic_from_contact_via_related_group(self):
        self.group_object.add_topic_to_contact(topic=Topic.objects.get(pk=2),
            contact=Contact.objects.get(pk=5))
        # Removes contact without needing override flag because relationship made via group.
        self.group_object.remove_topic_from_contact(topic=Topic.objects.get(pk=2),
            contact=Contact.objects.get(pk=5))
        self.assertEqual(0,
            len(TopicContactRelationship.objects.filter(topic_id=2, contact_id=5)))

    def test_remove_topic_from_contact_via_unrelated_group_when_topic_added_via_other_group(self):
        different_group = Group.objects.get(pk=4)
        different_group.add_topic_to_contact(topic=Topic.objects.get(pk=2),
            contact=Contact.objects.get(pk=5))
        # Won't remove because contact wasn't made via *this* group & override isn't passed.
        self.group_object.remove_topic_from_contact(topic=Topic.objects.get(pk=2),
            contact=Contact.objects.get(pk=5))
        self.assertEqual(1,
            len(TopicContactRelationship.objects.filter(topic_id=2, contact_id=5)))
        # Now will remove contact.
        self.group_object.remove_topic_from_contact(topic=Topic.objects.get(pk=2),
            contact=Contact.objects.get(pk=5), override=True)
        self.assertEqual(0,
            len(TopicContactRelationship.objects.filter(topic_id=2, contact_id=5)))

    def helper_for_manage_contacts(self):
        self.cordelia = Contact.objects.get(pk=5)
        self.willow = Contact.objects.get(pk=6)
        self.prom = Topic.objects.create(shortname="prom")
        self.different_group = Group.objects.create(shortname="non-Slayers")

    def test_manage_contacts_via_group_given_topic(self):
        self.helper_for_manage_contacts()
        self.group_object.contacts.add(self.cordelia, self.willow)
        self.group_object.manage_contacts_via_group("AddGivenTopic", topic=self.prom)
        self.assertEqual(['Cordelia', 'Willow Rosenberg'],
            [contact.shortname for contact in self.prom.contacts.all()])
        # Doesn't work because Cordelia and Willow are part of a different group.
        self.different_group.manage_contacts_via_group("RemoveGivenTopic", topic=self.prom)
        self.assertEqual(['Cordelia', 'Willow Rosenberg'],
            [contact.shortname for contact in self.prom.contacts.all()])
        # Does work when called on self.group_object
        self.group_object.manage_contacts_via_group("RemoveGivenTopic", topic=self.prom)
        self.assertEqual([],
            [contact.shortname for contact in self.prom.contacts.all()])

    def test_manage_contacts_via_group_given_related_contact(self):
        self.helper_for_manage_contacts()
        self.group_object.contacts.add(self.cordelia)
        # Doesn't work because group doesn't have a link to prom yet.
        self.group_object.manage_contacts_via_group("AddGivenContact", contact=self.cordelia)
        self.assertEqual([],
            [contact.shortname for contact in self.prom.contacts.all()])
        # Now it works
        self.group_object.topics.add(TopicGroupRelationship(group=self.group_object, topic=self.prom))
        self.group_object.manage_contacts_via_group("AddGivenContact", contact=self.cordelia)
        self.assertEqual(['Cordelia'],
            [contact.shortname for contact in self.prom.contacts.all()])
        self.group_object.manage_contacts_via_group("RemoveGivenContact", contact=self.cordelia)
        self.assertEqual([],
            [contact.shortname for contact in self.prom.contacts.all()])

    def test_manage_contacts_via_group_given_unrelated_contact(self):
        self.helper_for_manage_contacts()
        TopicContactRelationship.objects.create(topic=self.prom, contact=self.willow)
        self.group_object.topics.add(TopicGroupRelationship(group=self.group_object, topic=self.prom))
        # Removing Willow doesn't work without the override flag
        self.group_object.manage_contacts_via_group("RemoveGivenContact", contact=self.willow)
        self.assertEqual(['Willow Rosenberg'],
            [contact.shortname for contact in self.prom.contacts.all()])
        self.group_object.manage_contacts_via_group("RemoveGivenContact", contact=self.willow,
            override=True)
        self.assertEqual([],
            [contact.shortname for contact in self.prom.contacts.all()])
        self.group_object.manage_contacts_via_group("AddGivenContact", contact=self.willow)
        # However we can *add* the relationship even if Willow isn't part of the group
        self.assertEqual(['Willow Rosenberg'],
            [contact.shortname for contact in self.prom.contacts.all()])
        # And once we do, we can delete without needing an override
        self.group_object.manage_contacts_via_group("RemoveGivenContact", contact=self.willow)
        self.assertEqual([],
            [contact.shortname for contact in self.prom.contacts.all()])

class TestTopicModel(TestCase):

    fixtures = ['test_fixtures']

    def setUp(self):
        self.topic_object = Topic.objects.create(shortname="Magic")

    def test_contact_url(self):
        self.assertEqual("/topic/4/",
            self.topic_object.get_url())

    def test_get_group_pks(self):
        self.assertEqual(0,
            len(self.topic_object.get_group_pks()))
        relationship = TopicGroupRelationship.objects.create(topic=self.topic_object,
            group=Group.objects.get(pk=4))
        self.assertEqual(1,
            len(self.topic_object.get_group_pks()))
        relationship.delete()
        self.assertEqual(0,
            len(self.topic_object.get_group_pks()))

    def test_get_contact_pks(self):
        self.assertEqual(0,
            len(self.topic_object.get_contact_pks()))
        relationship = TopicContactRelationship.objects.create(topic=self.topic_object,
            contact=Contact.objects.get(pk=9))
        self.assertEqual(1,
            len(self.topic_object.get_contact_pks()))
        relationship.delete()
        self.assertEqual(0,
            len(self.topic_object.get_contact_pks()))

    def test_adjust_contact_by_adding_contacts(self):
        self.topic_object.adjust_contacts(set([2,3,4]))
        self.assertEqual(3,
            len(self.topic_object.contacts.all()))
        self.assertEqual(['Giles', 'Snyder', 'Spike'],
            [contact.shortname for contact in self.topic_object.contacts.all()])

    def test_adjust_contact_by_removing_contacts(self):
        TopicContactRelationship.objects.create(topic=self.topic_object,
            contact=Contact.objects.get(pk=2))
        TopicContactRelationship.objects.create(topic=self.topic_object,
                contact=Contact.objects.get(pk=3))
        self.assertEqual(2,
            len(self.topic_object.contacts.all()))
        self.topic_object.adjust_contacts(set([3]))
        self.assertEqual(1,
            len(self.topic_object.contacts.all()))
        self.assertEqual(['Giles'],
            [contact.shortname for contact in self.topic_object.contacts.all()])

    def test_adjust_group_by_adding_groups(self):
        self.topic_object.adjust_groups(set([4,5,6]))
        self.assertEqual(3,
            len(self.topic_object.group_set.all()))
        self.assertEqual(['People', 'Scoobies', 'Vampires'],
            [group.shortname for group in self.topic_object.group_set.all()])

    def test_adjust_group_by_removing_groups(self):
        TopicGroupRelationship.objects.create(topic=self.topic_object,
            group=Group.objects.get(pk=4))
        TopicGroupRelationship.objects.create(topic=self.topic_object,
            group=Group.objects.get(pk=5))
        self.assertEqual(2,
            len(self.topic_object.group_set.all()))
        self.topic_object.adjust_groups(set([5]))
        self.assertEqual(1,
            len(self.topic_object.group_set.all()))
        self.assertEqual(['Scoobies'],
            [group.shortname for group in self.topic_object.group_set.all()])


########################
### Utils Unit Tests ###
########################

class TestTopicObjectToggling(TestCase):

    fixtures = ['test_fixtures']

    def setUp(self):
        self.object_to_update = Topic.objects.get(pk=1)
        self.linked_contact = Contact.objects.get(shortname="Faith")

    def test_local_toggle_archive(self):
        self.assertEquals(False,
            self.object_to_update.archived)
        self.object_to_update = local_toggle(self.object_to_update, "archive")
        self.assertEquals(True,
            self.object_to_update.archived)
        self.object_to_update = local_toggle(self.object_to_update, "archive")
        self.assertEquals(False,
            self.object_to_update.archived)

    def test_local_toggle_star(self):
        self.assertEquals(False,
            self.object_to_update.starred)
        self.object_to_update = local_toggle(self.object_to_update, "star")
        self.assertEquals(True,
            self.object_to_update.starred)
        self.object_to_update = local_toggle(self.object_to_update, "star")
        self.assertEquals(False,
            self.object_to_update.starred)

    def test_global_toggle_of_topic_object_archive(self):
        self.assertEquals(False,
            self.object_to_update.archived)
        self.assertEquals(3,
            len([topic for topic in self.linked_contact.topics.all() if topic.archived is False]))
        self.object_to_update = global_toggle(self.object_to_update, "archive")
        self.assertEquals(True,
            self.object_to_update.archived)
        self.assertEquals(2,
            len([topic for topic in self.linked_contact.topics.all() if topic.archived is False]))
        self.object_to_update = global_toggle(self.object_to_update, "archive")
        self.assertEquals(False,
            self.object_to_update.archived)
        self.assertEquals(3,
            len([topic for topic in self.linked_contact.topics.all() if topic.archived is False]))

    def test_global_toggle_of_topic_object_starred(self):
        self.assertEquals(False,
            self.object_to_update.starred)
        self.assertEquals(False,
            self.linked_contact.topics.get(pk=self.object_to_update.pk).starred)
        self.object_to_update = global_toggle(self.object_to_update, "star")
        self.assertEquals(True,
            self.object_to_update.starred)
        self.assertEquals(True,
            self.linked_contact.topics.get(pk=self.object_to_update.pk).starred)
        self.object_to_update = global_toggle(self.object_to_update, "star")
        self.assertEquals(False,
            self.object_to_update.starred)
        self.assertEquals(False,
            self.linked_contact.topics.get(pk=self.object_to_update.pk).starred)

    def test_global_then_local_toggle_topic_object_archive(self):
        self.object_to_update = global_toggle(self.object_to_update, "archive")
        # test_global_toggle_of_topic_object_archive tests above behavior
        self.object_to_update = local_toggle(self.object_to_update, "archive")
        self.assertEquals(False,
            self.object_to_update.archived)
        self.assertEquals(2,
            len([topic for topic in self.linked_contact.topics.all() if topic.archived is False]))

### Runs the above cases but on relationship objects
class TestTopicContactRelationshipToggling(TestTopicObjectToggling):

    def setUp(self):
        self.object_to_update = TopicContactRelationship.objects.get(pk=1)
        self.linked_contact = Contact.objects.get(shortname="Faith")

class TestTopicGroupRelationshipToggling(TestTopicObjectToggling):

    def setUp(self):
        self.object_to_update = TopicGroupRelationship.objects.get(pk=1)
        self.linked_contact = Contact.objects.get(shortname="Faith")


##############################
### AJAXy Views Unit Tests ###
##############################
class TestUpdateManagerView(TestCase):

    fixtures = ['test_fixtures']

    def setUp(self):
        self.client = Client()

    def helper_post_data_and_parse_response(self, data):
        response = self.client.post(reverse('update_manager'), data)
        return json.loads(response.content.decode())['current_dict']

    def test_add_groups_to_contact(self):
        manage_form = json.dumps([{"pk":"4","checked":True}, {"pk":"5","checked":True},
            {"pk":"6","checked":True}])
        response = self.helper_post_data_and_parse_response({'object_type_to_adjust': 'group',
            'object_type': 'contact', 'object_pk': '5', 'manage_form': manage_form })
        self.assertEquals(3, len(response))
        self.assertEqual(3, len(Contact.objects.get(pk=5).group_set.all()))

    def test_remove_groups_from_contact(self):
        self.assertEqual(2, len(Contact.objects.get(pk=8).group_set.all()))
        manage_form = json.dumps([{"pk":"4","checked":False}, {"pk":"5","checked":False},
            {"pk":"6","checked":False}])
        response = self.helper_post_data_and_parse_response({'object_type_to_adjust': 'group',
            'object_type': 'contact', 'object_pk': '9', 'manage_form': manage_form })
        self.assertEquals(0, len(response))
        self.assertEqual(0, len(Contact.objects.get(pk=9).group_set.all()))

    def test_add_topics_to_contact(self):
        manage_form = json.dumps([{"pk":"1","checked":True}, {"pk":"2","checked":True},
            {"pk":"3","checked":True}])
        response = self.helper_post_data_and_parse_response({'object_type_to_adjust': 'topic',
            'object_type': 'contact', 'object_pk': '4', 'manage_form': manage_form })
        self.assertEquals(3, len(response))
        self.assertEqual(3, len(Contact.objects.get(pk=4).topics.all()))

    def test_remove_topics_from_contact(self):
        self.assertEqual(3, len(Contact.objects.get(pk=9).topics.all()))
        manage_form = json.dumps([{"pk":"1","checked":False}, {"pk":"2","checked":False},
            {"pk":"3","checked":False}])
        response = self.helper_post_data_and_parse_response({'object_type_to_adjust': 'topic',
            'object_type': 'contact', 'object_pk': '9', 'manage_form': manage_form })
        self.assertEquals(0, len(response))
        self.assertEqual(0, len(Contact.objects.get(pk=9).topics.all()))

    def test_return_different_dicts_for_topic_than_contact_or_group(self):
        manage_form = json.dumps([{"pk":"1","checked":True}, {"pk":"2","checked":True},
            {"pk":"3","checked":True}])
        topic_response = self.helper_post_data_and_parse_response({'object_type_to_adjust': 'topic',
            'object_type': 'contact', 'object_pk': '9', 'manage_form': manage_form })
        manage_form = json.dumps([{"pk":"4","checked":True}, {"pk":"5","checked":True},
            {"pk":"6","checked":True}])
        group_response = self.helper_post_data_and_parse_response({'object_type_to_adjust': 'group',
            'object_type': 'contact', 'object_pk': '5', 'manage_form': manage_form })
        manage_form = json.dumps([{"pk":"3","checked":True}, {"pk":"2","checked":True},
            {"pk":"4","checked":True}])
        contact_response = self.helper_post_data_and_parse_response({'object_type_to_adjust': 'contact',
            'object_type': 'group', 'object_pk': '5', 'manage_form': manage_form })
        self.assertTrue('url' in topic_response[0])
        self.assertTrue('url' in contact_response[0])
        self.assertTrue('url' in group_response[0])
        self.assertTrue('archived' in topic_response[0])
        self.assertFalse('archived' in contact_response[0])
        self.assertFalse('archived' in group_response[0])

class TestToggleTopicView(TestCase):

    fixtures = ['test_fixtures']

    def setUp(self):
        self.client = Client()

    def helper_post_data_and_parse_response(self, data):
        response = self.client.post(reverse('toggle_topic'), data)
        return json.loads(json.loads(response.content.decode()))['topic_data']

    def test_archive_topic_object_locally(self):
        response = self.helper_post_data_and_parse_response({'toggle_type': 'archive',
            'toggle_scope': 0, 'topic_pk': 1, 'object_type': 'topic', 'object_pk': 1})
        self.assertTrue(response['archived'])
        self.assertFalse(response['starred'])
        self.assertTrue(Topic.objects.get(pk=1).archived)
        self.assertFalse(Topic.objects.get(pk=1).starred)

    def test_archive_topic_object_globally(self):
        response = self.helper_post_data_and_parse_response({'toggle_type': 'archive',
            'toggle_scope': 1, 'topic_pk': 1, 'object_type': 'topic', 'object_pk': 1})
        self.assertTrue(response['archived'])
        self.assertFalse(response['starred'])
        self.assertTrue(Topic.objects.get(pk=1).archived)
        self.assertFalse(Topic.objects.get(pk=1).starred)

    def test_star_topic_object_locally(self):
        response = self.helper_post_data_and_parse_response({'toggle_type': 'star',
            'toggle_scope': 0, 'topic_pk': 1, 'object_type': 'topic', 'object_pk': 1})
        self.assertFalse(response['archived'])
        self.assertTrue(response['starred'])
        self.assertFalse(Topic.objects.get(pk=1).archived)
        self.assertTrue(Topic.objects.get(pk=1).starred)

    def test_star_topic_object_globally(self):
        response = self.helper_post_data_and_parse_response({'toggle_type': 'star',
            'toggle_scope': 1, 'topic_pk': 1, 'object_type': 'topic', 'object_pk': 1})
        self.assertFalse(response['archived'])
        self.assertTrue(response['starred'])
        self.assertFalse(Topic.objects.get(pk=1).archived)
        self.assertTrue(Topic.objects.get(pk=1).starred)

    def test_archive_contact_topic_object_locally(self):
        response = self.helper_post_data_and_parse_response({'toggle_type': 'archive',
            'toggle_scope': 0, 'topic_pk': 1, 'object_type': 'contact', 'object_pk': 9})
        self.assertTrue(response['archived'])
        self.assertFalse(response['starred'])
        self.assertTrue(TopicContactRelationship.objects.get(pk=1).archived)
        self.assertFalse(TopicContactRelationship.objects.get(pk=1).starred)

    def test_archive_contact_topic_object_globally(self):
        response = self.helper_post_data_and_parse_response({'toggle_type': 'archive',
            'toggle_scope': 1, 'topic_pk': 1, 'object_type': 'contact', 'object_pk': 9})
        self.assertTrue(response['archived'])
        self.assertFalse(response['starred'])
        self.assertTrue(TopicContactRelationship.objects.get(pk=1).archived)
        self.assertFalse(TopicContactRelationship.objects.get(pk=1).starred)

    def test_star_contact_topic_object_locally(self):
        response = self.helper_post_data_and_parse_response({'toggle_type': 'star',
            'toggle_scope': 0, 'topic_pk': 1, 'object_type': 'contact', 'object_pk': 9})
        self.assertFalse(response['archived'])
        self.assertTrue(response['starred'])
        self.assertFalse(TopicContactRelationship.objects.get(pk=1).archived)
        self.assertTrue(TopicContactRelationship.objects.get(pk=1).starred)

    def test_star_contact_topic_object_globally(self):
        response = self.helper_post_data_and_parse_response({'toggle_type': 'star',
            'toggle_scope': 1, 'topic_pk': 1, 'object_type': 'contact', 'object_pk': 9})
        self.assertFalse(response['archived'])
        self.assertTrue(response['starred'])
        self.assertFalse(TopicContactRelationship.objects.get(pk=1).archived)
        self.assertTrue(TopicContactRelationship.objects.get(pk=1).starred)

    def test_archive_group_topic_object_locally(self):
        response = self.helper_post_data_and_parse_response({'toggle_type': 'archive',
            'toggle_scope': 0, 'topic_pk': 2, 'object_type': 'group', 'object_pk': 4})
        self.assertTrue(response['archived'])
        self.assertFalse(response['starred'])
        self.assertTrue(TopicGroupRelationship.objects.get(pk=1).archived)
        self.assertFalse(TopicGroupRelationship.objects.get(pk=1).starred)

    def test_archive_group_topic_object_globally(self):
        response = self.helper_post_data_and_parse_response({'toggle_type': 'archive',
            'toggle_scope': 1, 'topic_pk': 2, 'object_type': 'group', 'object_pk': 4})
        self.assertTrue(response['archived'])
        self.assertFalse(response['starred'])
        self.assertTrue(TopicGroupRelationship.objects.get(pk=1).archived)
        self.assertFalse(TopicGroupRelationship.objects.get(pk=1).starred)

    def test_star_group_topic_object_locally(self):
        response = self.helper_post_data_and_parse_response({'toggle_type': 'star',
            'toggle_scope': 0, 'topic_pk': 2, 'object_type': 'group', 'object_pk': 4})
        self.assertFalse(response['archived'])
        self.assertTrue(response['starred'])
        self.assertFalse(TopicGroupRelationship.objects.get(pk=1).archived)
        self.assertTrue(TopicGroupRelationship.objects.get(pk=1).starred)

    def test_star_group_topic_object_globally(self):
        response = self.helper_post_data_and_parse_response({'toggle_type': 'star',
            'toggle_scope': 1, 'topic_pk': 2, 'object_type': 'group', 'object_pk': 4})
        self.assertFalse(response['archived'])
        self.assertTrue(response['starred'])
        self.assertFalse(TopicGroupRelationship.objects.get(pk=1).archived)
        self.assertTrue(TopicGroupRelationship.objects.get(pk=1).starred)
