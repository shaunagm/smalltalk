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

def update_manager(request):
    posted_form = request.POST.get('manage_form', None)
    object_type = request.POST.get('object_type', None)
    object_pk = request.POST.get('object_pk', None)
    if posted_form and object_type and object_pk:
        form_data = json.loads(posted_form)
        selected_items = set([int(item['pk']) for item in form_data
            if item['checked'] == True])
        if object_type == "Contact":
            main_object = Contact.objects.get(pk = int(object_pk))
            final_items = main_object.adjust_groups(selected_items)
        if object_type == "Group":
            main_object = Group.objects.get(pk = int(object_pk))
            final_items = main_object.adjust_contacts(selected_items)
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
