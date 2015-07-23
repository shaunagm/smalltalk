import json
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.http import JsonResponse

from .models import Contact, Group, Topic
from .forms import ContactForm, GroupForm, TopicForm, ManageContactsForm, ManageGroupsForm

from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render

from .utils import group_form_helper, contact_form_helper, topic_form_helper

####################
#### Meta Views ####
####################

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['ContactForm'] = ContactForm(prefix="contact")
        context['GroupForm'] = GroupForm(prefix="group")
        return context

#####################
### Contact Views ###
#####################

class ContactList(ListView):
    model = Contact
    template_name = "list.html"

    def get_context_data(self, **kwargs):
        context = super(ContactList, self).get_context_data(**kwargs)
        context['object_type'] = "Contacts"
        return context

class ContactDetail(DetailView):
    model = Contact
    template_name = "contact.html"

    def get_context_data(self, **kwargs):
        context = super(ContactDetail, self).get_context_data(**kwargs)
        context.update(group_form_helper(self.object))
        context.update(topic_form_helper(self.object))
        context['object_type'] = "Contact"
        return context

class ContactCreate(CreateView):
    form_class = ContactForm
    template_name = "contact_edit.html"

    def get_success_url(self, **kwargs):
        return self.object.get_url()

class ContactEdit(UpdateView):
    model = Contact
    fields = ['shortname', 'details']
    template_name = "contact_edit.html"

    def get_success_url(self, **kwargs):
        return self.object.get_url()

###################
### Group Views ###
###################

class GroupCreate(CreateView):
    form_class = GroupForm
    template_name = "group_edit.html"

    def get_success_url(self, **kwargs):
        return self.object.get_url()

class GroupDetail(DetailView):
    model = Group
    template_name = "group.html"

    def get_context_data(self, **kwargs):
        context = super(GroupDetail, self).get_context_data(**kwargs)
        context.update(contact_form_helper(self.object))
        context.update(topic_form_helper(self.object))
        context['object_type'] = "Group"
        return context

class GroupEdit(UpdateView):
    model = Group
    fields = ['shortname', 'details']
    template_name = "group_edit.html"

    def get_success_url(self, **kwargs):
        return self.object.get_url()

class GroupList(ListView):
    model = Group
    template_name = "list.html"

    def get_context_data(self, **kwargs):
        context = super(GroupList, self).get_context_data(**kwargs)
        context['object_type'] = "Groups"
        return context

###################
### Topic Views ###
###################

class TopicList(ListView):
    model = Topic
    template_name = "list.html"

    def get_context_data(self, **kwargs):
        context = super(TopicList, self).get_context_data(**kwargs)
        context['object_type'] = "Topics"
        return context

class TopicDetail(DetailView):
    model = Topic
    template_name = "topic.html"

    def get_context_data(self, **kwargs):
        context = super(TopicDetail, self).get_context_data(**kwargs)
        context.update(contact_form_helper(self.object))
        context.update(group_form_helper(self.object))
        context['object_type'] = "Topic"
        return context

class TopicCreate(CreateView):
    form_class = TopicForm
    template_name = "topic_edit.html"

    def get_success_url(self, **kwargs):
        return self.object.get_url()

class TopicEdit(UpdateView):
    model = Topic
    fields = ['shortname', 'details', 'link']
    template_name = "topic_edit.html"

    def get_success_url(self, **kwargs):
        return self.object.get_url()


###################
### AJAXy Views ###
###################

def update_manager(request):
    posted_form = request.POST.get('manage_form', None)
    object_type = request.POST.get('object_type', None)
    object_pk = request.POST.get('object_pk', None)
    object_type_to_adjust =  request.POST.get('object_type_to_adjust', None)
    if posted_form and object_type and object_pk and object_type_to_adjust:
        form_data = json.loads(posted_form)
        selected_items = set([int(item['pk']) for item in form_data
            if item['checked'] == True])
        if object_type == "Contact":
            main_object = Contact.objects.get(pk = int(object_pk))
            if object_type_to_adjust == "Group":
                final_items = main_object.adjust_groups(selected_items)
            if object_type_to_adjust == "Topic":
                final_items = main_object.adjust_topics(selected_items)
        if object_type == "Topic":
            main_object = Topic.objects.get(pk = int(object_pk))
            if object_type_to_adjust == "Contact":
                final_items = main_object.adjust_contacts(selected_items)
            if object_type_to_adjust == "Group":
                final_items = main_object.adjust_groups(selected_items)
        if object_type == "Group":
            main_object = Group.objects.get(pk = int(object_pk))
            if object_type_to_adjust == "Contact":
                final_items = main_object.adjust_contacts(selected_items)
            if object_type_to_adjust == "Topic":
                final_items = main_object.adjust_topics(selected_items)
        current_dict = [{'name': item.shortname, 'url': item.get_url()}
            for item in final_items]
        return JsonResponse({'status': 'Success', 'current_dict': current_dict})
    return JsonResponse(json.dumps({'status': 'There was a servor error.'}), safe=False)

def create_new_contact(request):
    name = request.POST.get('name', None)
    details = request.POST.get('details', None)
    if name:
        contact, created = Contact.objects.get_or_create(name=name,
            defaults={'details' : details})
        if created:
            return JsonResponse(json.dumps({'status': 'success',
                'name': contact.shortname, 'url': contact.get_url()}), safe=False)
        else:
            return JsonResponse(json.dumps({'status': 'error',
                'message': 'This contact already exists.'}), safe=False)
    else:
        return JsonResponse(json.dumps({'status': 'error',
            'message': 'The name field is required.'}), safe=False)

def create_new_group(request):
    name = request.POST.get('name', None)
    details = request.POST.get('details', None)
    if name:
        group, created = Group.objects.get_or_create(name=name,
            defaults={'details' : details})
        if created:
            return JsonResponse(json.dumps({'status': 'success',
                'name': group.shortname, 'url': group.get_url()}), safe=False)
        else:
            return JsonResponse(json.dumps({'status': 'error',
                'message': 'This group already exists.'}), safe=False)
    else:
        return JsonResponse(json.dumps({'status': 'error',
            'message': 'The name field is required.'}), safe=False)
