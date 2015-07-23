from django.db import models
from django.core.urlresolvers import reverse

class Contact(models.Model):
    shortname = models.CharField(max_length=100, unique=True)
    details = models.TextField(max_length=5000, blank=True)

    def name(self):
        return self.shortname

    def __str__(self):
        return self.shortname

    def get_url(self):
        return reverse('contact_detail', args=[self.pk])

    def get_group_pks(self):
        return set([group.pk for group in self.group_set.all()])

    def get_topic_pks(self):
        return set([topic.pk for topic in self.topic_set.all()])

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
            self.topic_set.add(topic)
        for pk in topic_pks - pk_set:
            topic = Topic.objects.get(pk=pk)
            self.topic_set.remove(topic)
        return self.topic_set.all()

class Group(models.Model):
    shortname = models.CharField(max_length=100, unique=True)
    details = models.TextField(max_length=5000, blank=True)
    contacts = models.ManyToManyField(Contact)

    def name(self):
        return self.shortname

    def __str__(self):
        return self.shortname

    def get_url(self):
        return reverse('group_detail', args=[self.pk])

    def get_contact_pks(self):
        return set([contact.pk for contact in self.contacts.all()])

    def get_topic_pks(self):
        return set([topic.pk for topic in self.topic_set.all()])

    def adjust_contacts(self, pk_set):
        contact_pks = self.get_contact_pks()
        for pk in pk_set - contact_pks:
            contact = Contact.objects.get(pk=pk)
            self.contacts.add(contact)
        for pk in contact_pks - pk_set:
            contact = Contact.objects.get(pk=pk)
            self.contacts.remove(contact)
        return self.contacts.all()

    def adjust_topics(self, pk_set):
        topic_pks = self.get_topic_pks()
        for pk in pk_set - topic_pks:
            topic = Topic.objects.get(pk=pk)
            self.topic_set.add(topic)
        for pk in topic_pks - pk_set:
            topic = Topic.objects.get(pk=pk)
            self.topic_set.remove(topic)
        return self.topic_set.all()

class Topic(models.Model):
    shortname = models.CharField(max_length=100, unique=True)
    details = models.TextField(max_length=5000, blank=True)
    link = models.CharField(max_length=200, blank=True)
    contacts = models.ManyToManyField(Contact)
    group_set = models.ManyToManyField(Group)

    def name(self):
        return self.shortname

    def __str__(self):
        return self.shortname

    def get_url(self):
        return reverse('topic_detail', args=[self.pk])

    def get_group_pks(self):
        return set([group.pk for group in self.group_set.all()])

    def get_contact_pks(self):
        return set([contact.pk for contact in self.contacts.all()])

    def adjust_contacts(self, pk_set):
        contact_pks = self.get_contact_pks()
        for pk in pk_set - contact_pks:
            contact = Contact.objects.get(pk=pk)
            self.contacts.add(contact)
        for pk in contact_pks - pk_set:
            contact = Contact.objects.get(pk=pk)
            self.contacts.remove(contact)
        return self.contacts.all()

    def adjust_groups(self, pk_set):
        group_pks = self.get_group_pks()
        for pk in pk_set - group_pks:
            group = Group.objects.get(pk=pk)
            self.group_set.add(group)
        for pk in group_pks - pk_set:
            group = Group.objects.get(pk=pk)
            self.group_set.remove(group)
        return self.group_set.all()
