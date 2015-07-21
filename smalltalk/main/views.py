import json
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.http import JsonResponse

from .models import Contact, Group
from .forms import ContactForm, GroupForm, ManageContactsForm, ManageGroupsForm

from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render

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
        if Group.objects.all():
            context['manage_group_form'] = ManageGroupsForm(contact=self.object)
        else:
            context['no_groups_message'] = "You do not have any groups.  Why don't you" \
                " try <a href='/group/new/'>adding some</a>?"
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
        if Contact.objects.all():
            context['manage_contact_form'] = ManageContactsForm(group=self.object)
        else:
            context['no_contacts_message'] = "You do not have any contacts.  Why don't you" \
                " try <a href='/contact/new/'>adding some</a>?"
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
### AJAXy Views ###
###################

def update_group_manager(request):
    posted_form = request.POST.get('group_manage_form', None)
    grouped_object_type = request.POST.get('grouped_object_type', None)
    grouped_object_pk = request.POST.get('grouped_object_pk', None)
    if posted_form and grouped_object_type and grouped_object_pk:
        if grouped_object_type == "Contact":
            grouped_object = Contact.objects.get(pk = int(grouped_object_pk))
        else:
            pass # Topic object goes here.
        form_data = json.loads(posted_form)
        selected_groups = set([int(group['pk']) for group in form_data
            if group['checked'] == True])
        grouped_object.adjust_groups(selected_groups)
        current_group_dict = [{'name': group.shortname, 'url': group.get_url()}
            for group in grouped_object.group_set.all()]
        return JsonResponse({'status': 'Success', 'current_groups': current_group_dict})
    return JsonResponse(json.dumps({'status': 'There was a servor error.'}), safe=False)

def update_contact_manager(request):
    posted_form = request.POST.get('contact_manage_form', None)
    contacted_object_type = request.POST.get('contacted_object_type', None)
    contacted_object_pk = request.POST.get('contacted_object_pk', None)
    if posted_form and contacted_object_type and contacted_object_pk:
        if contacted_object_type == "Group":
            contacted_object = Group.objects.get(pk = int(contacted_object_pk))
        else:
            pass # Topic object goes here.
        form_data = json.loads(posted_form)
        selected_contacts = set([int(contact['pk']) for contact in form_data
            if contact['checked'] == True])
        contacted_object.adjust_contacts(selected_contacts)
        current_contact_dict = [{'name': contact.shortname, 'url': contact.get_url()}
            for contact in contacted_object.contacts.all()]
        return JsonResponse({'status': 'Success', 'current_contacts': current_contact_dict})
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
