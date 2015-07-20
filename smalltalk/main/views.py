import json
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.http import JsonResponse

from .models import Contact, Group
from .forms import ContactForm, GroupForm

from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['ContactForm'] = ContactForm(prefix="contact")
        context['GroupForm'] = GroupForm(prefix="group")
        return context

### Contact Views ###

class ContactList(ListView):
    model = Contact
    template_name = "list.html"

    def get_context_data(self, **kwargs):
        context = super(ContactList, self).get_context_data(**kwargs)
        context['object_type'] = "Contacts"
        return context

class ContactCreate(CreateView):
    form_class = ContactForm
    template_name = "contact_edit.html"

    def get_success_url(self, **kwargs):
        return self.object.get_url()

# Works with AJAX for inline contact creation
def create_new_contact(request):
    name = request.POST.get('name', None)
    details = request.POST.get('details', None)
    if name:
        contact, created = Contact.objects.get_or_create(name=name,
            defaults={'details' : details})
        if created:
            return JsonResponse(json.dumps({'status': 'success',
                'name': contact.name, 'url': contact.get_url()}), safe=False)
        else:
            return JsonResponse(json.dumps({'status': 'error',
                'message': 'This contact already exists.'}), safe=False)
    else:
        return JsonResponse(json.dumps({'status': 'error',
            'message': 'The name field is required.'}), safe=False)

class ContactDetail(DetailView):
    model = Contact
    template_name = "contact.html"

class ContactEdit(UpdateView):
    model = Contact
    fields = ['name', 'details']
    template_name = "contact_edit.html"

    def get_success_url(self, **kwargs):
        return self.object.get_url()

### Group Views ###

class GroupCreate(CreateView):
    form_class = GroupForm
    template_name = "group_edit.html"

    def get_success_url(self, **kwargs):
        return self.object.get_url()

def create_new_group(request):
    name = request.POST.get('name', None)
    details = request.POST.get('details', None)
    if name:
        group, created = Group.objects.get_or_create(name=name,
            defaults={'details' : details})
        if created:
            return JsonResponse(json.dumps({'status': 'success',
                'name': group.name, 'url': group.get_url()}), safe=False)
        else:
            return JsonResponse(json.dumps({'status': 'error',
                'message': 'This group already exists.'}), safe=False)
    else:
        return JsonResponse(json.dumps({'status': 'error',
            'message': 'The name field is required.'}), safe=False)

class GroupDetail(DetailView):
    model = Group
    template_name = "group.html"

class GroupEdit(UpdateView):
    model = Group
    fields = ['name', 'details']
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

def manage_groups_for_contact(request):
    name = request.POST.get('name', None)
    if name:
        contact = Contact.objects.get(name=name)
        groups = Group.objects.all()
        responses = []
        for group in groups:
            in_group = 1 if contact in group.contacts.all() else 0
            responses.append({'group_name': group.name, 'in_group': in_group})
        if len(responses) > 0:
            return JsonResponse(json.dumps({'status': 'success', 'data': responses}), safe=False)
        else:
            return JsonResponse(json.dumps({'status': 'Please create some groups.'}), safe=False)
    return JsonResponse(json.dumps({'status': 'There was a servor error.'}), safe=False)
