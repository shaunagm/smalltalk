from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import ContactForm

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['ContactForm'] = ContactForm()
        return context
