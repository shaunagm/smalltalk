from django.db import models
from django.core.urlresolvers import reverse

# Custom Managers
class CustomContactManager(models.Manager):
    def get_queryset(self):
        return super(CustomContactManager, self).get_queryset().order_by('shortname')

class CustomGroupManager(models.Manager):
    def get_queryset(self):
        return super(CustomGroupManager, self).get_queryset().order_by('shortname')

class CustomTopicManager(models.Manager):
    def get_queryset(self):
        return super(CustomTopicManager, self).get_queryset().exclude(archived=1)


# Models
class Contact(models.Model):
    shortname = models.CharField(max_length=100, unique=True)
    details = models.TextField(max_length=5000, blank=True)

    objects = CustomContactManager()

    def name(self):
        return self.shortname

    def __str__(self):
        return self.shortname

    def get_url(self):
        return reverse('contact_detail', args=[self.pk])

    def get_group_pks(self):
        return set([group.pk for group in self.group_set.all()])

    def get_topic_pks(self):
        return set([relationship.topic.pk for relationship
            in self.topiccontactrelationship_set.all()])

    def adjust_groups(self, pk_set):
        group_pks = self.get_group_pks()
        for pk in pk_set - group_pks:
            group = Group.objects.get(pk=pk)
            self.group_set.add(group)
        for pk in group_pks - pk_set:
            group = Group.objects.get(pk=pk)
            self.group_set.remove(group)
        return self.group_set.all()

    def adjust_topics(self, pk_set):
        topic_pks = self.get_topic_pks()
        for pk in pk_set - topic_pks:
            topic = Topic.objects.get(pk=pk)
            relationship = TopicContactRelationship(contact=self, topic=topic)
            relationship.save()
        for pk in topic_pks - pk_set:
            topic = Topic.objects.get(pk=pk)
            relationship = TopicContactRelationship.objects.get(contact=self, topic=topic)
            relationship.delete()
        return self.topic_set.all()

class Group(models.Model):
    shortname = models.CharField(max_length=100, unique=True)
    details = models.TextField(max_length=5000, blank=True)
    contacts = models.ManyToManyField(Contact)

    objects = CustomGroupManager()

    def name(self):
        return self.shortname

    def __str__(self):
        return self.shortname

    def get_url(self):
        return reverse('group_detail', args=[self.pk])

    def get_contact_pks(self):
        return set([contact.pk for contact in self.contacts.all()])

    def get_topic_pks(self):
        return set([relationship.topic.pk for relationship
            in self.topicgrouprelationship_set.all()])

    def adjust_contacts(self, pk_set):
        contact_pks = self.get_contact_pks()
        for pk in pk_set - contact_pks:
            contact = Contact.objects.get(pk=pk)
            self.contacts.add(contact)
            self.manage_contacts_via_group(contact=contact, adjust_type="AddGivenContact")
        for pk in contact_pks - pk_set:
            contact = Contact.objects.get(pk=pk)
            self.contacts.remove(contact)
            self.manage_contacts_via_group(contact=contact, adjust_type="RemoveGivenContact")
        return self.contacts.all()

    def adjust_topics(self, pk_set):
        topic_pks = self.get_topic_pks()
        for pk in pk_set - topic_pks:
            topic = Topic.objects.get(pk=pk)
            relationship = TopicGroupRelationship(group=self, topic=topic)
            relationship.save()
            self.manage_contacts_via_group(topic=topic, adjust_type="AddGivenTopic")
        for pk in topic_pks - pk_set:
            topic = Topic.objects.get(pk=pk)
            relationship = TopicGroupRelationship.objects.get(group=self, topic=topic)
            relationship.delete()
            self.manage_contacts_via_group(topic=topic, adjust_type="RemoveGivenTopic")
        return self.topic_set.all()

    def manage_contacts_via_group(self, adjust_type, topic=[], contact=[], override=False):
        if adjust_type == "AddGivenTopic":
            for contact in self.contacts.all():
                self.add_topic_to_contact(topic, contact)
        if adjust_type == "RemoveGivenTopic":
            for contact in self.contacts.all():
                self.remove_topic_from_contact(topic, contact, override)
        if adjust_type == "AddGivenContact":
            for topic in self.topic_set.all():
                self.add_topic_to_contact(topic, contact)
        if adjust_type == "RemoveGivenContact":
            for topic in self.topic_set.all():
                self.remove_topic_from_contact(topic, contact, override)

    def add_topic_to_contact(self, topic, contact):
        relationship_set = TopicContactRelationship.objects.filter(contact=contact,
            topic=topic)
        if not relationship_set:
            relationship = TopicContactRelationship(contact=contact,
                topic=topic, via_group=1, via_group_name=self)
            relationship.save()

    def remove_topic_from_contact(self, topic, contact, override=False):
        relationship_set = TopicContactRelationship.objects.filter(
            contact=contact, topic=topic)
        if relationship_set:
            '''Only deletes relationship if previously made via this group
            or if an override flag has been passed.'''
            rel = relationship_set[0]
            if rel.via_group and (rel.via_group_name == self):
                rel.delete()
            elif override:
                rel.delete()

class Topic(models.Model):
    shortname = models.CharField(max_length=100, unique=True)
    details = models.TextField(max_length=5000, blank=True)
    link = models.CharField(max_length=200, blank=True)
    archived = models.BooleanField(default=False)
    contacts = models.ManyToManyField(Contact, through='TopicContactRelationship')
    group_set = models.ManyToManyField(Group, through='TopicGroupRelationship')

    objects = CustomTopicManager()

    def name(self):
        return self.shortname

    def __str__(self):
        return self.shortname

    def get_url(self):
        return reverse('topic_detail', args=[self.pk])

    def get_group_pks(self):
        return set([relationship.group.pk for relationship
            in self.topicgrouprelationship_set.all()])

    def get_contact_pks(self):
        return set([relationship.contact.pk for relationship
            in self.topiccontactrelationship_set.all()])

    def adjust_contacts(self, pk_set):
        contact_pks = self.get_contact_pks()
        for pk in pk_set - contact_pks:
            contact = Contact.objects.get(pk=pk)
            relationship = TopicContactRelationship(topic=self, contact=contact)
            relationship.save()
        for pk in contact_pks - pk_set:
            contact = Contact.objects.get(pk=pk)
            relationship = TopicContactRelationship.objects.get(topic=self, contact=contact)
            relationship.delete()
        return self.contacts.all()

    def adjust_groups(self, pk_set):
        group_pks = self.get_group_pks()
        for pk in pk_set - group_pks:
            group = Group.objects.get(pk=pk)
            relationship = TopicGroupRelationship(topic=self, group=group)
            relationship.save()
        for pk in group_pks - pk_set:
            group = Group.objects.get(pk=pk)
            relationship = TopicGroupRelationship.objects.get(topic=self, group=group)
            relationship.delete()
        return self.group_set.all()

class TopicContactRelationship(models.Model):
    topic = models.ForeignKey(Topic)
    contact = models.ForeignKey(Contact)
    archived = models.BooleanField(default=False)
    via_group = models.BooleanField(default=False)
    via_group_name = models.ForeignKey(Group, null=True)

    objects = CustomTopicManager()

class TopicGroupRelationship(models.Model):
    topic = models.ForeignKey(Topic)
    group = models.ForeignKey(Group)
    archived = models.BooleanField(default=False)

    objects = CustomTopicManager()
