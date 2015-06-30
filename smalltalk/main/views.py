import json
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.http import JsonResponse

from .models import Contact
from .forms import ContactForm

from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['ContactForm'] = ContactForm()
        return context

def create_new_contact(request):
    name = request.POST.get('name', None)
    details = request.POST.get('details', None)
    if name:
        contact, created = Contact.objects.get_or_create(name=name, details=details)
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
