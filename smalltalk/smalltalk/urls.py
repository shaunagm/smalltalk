from django.conf.urls import url
from django.views.decorators.csrf import ensure_csrf_cookie

from main import views

urlpatterns = [
    url(r'^$', ensure_csrf_cookie(views.IndexView.as_view()), name='home'),
    url(r'^contact/(?P<pk>[0-9]+)/$', views.ContactDetail.as_view(), name='contact_detail'),
    url(r'^new_contact$', views.create_new_contact, name='new_contact'),
    # url(r'^admin/', include(admin.site.urls)),
]
