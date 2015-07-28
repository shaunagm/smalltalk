from django.conf.urls import url
from django.views.decorators.csrf import ensure_csrf_cookie

from main import views

urlpatterns = [
    url(r'^$', ensure_csrf_cookie(views.IndexView.as_view()), name='home'),

    url(r'^contact/all/$', views.ContactList.as_view(), name='contact_list_view'),
    url(r'^contact/new/$', views.ContactCreate.as_view(), name='new_contact_view'),
    url(r'^contact/(?P<pk>[0-9]+)/$', views.ContactDetail.as_view(), name='contact_detail'),
    url(r'^contact/(?P<pk>[0-9]+)/edit$', views.ContactEdit.as_view(), name='contact_edit'),
    url(r'^new_contact$', views.create_new_contact, name='new_contact'),

    url(r'^group/all/$', views.GroupList.as_view(), name='group_list_view'),
    url(r'^group/new/$', views.GroupCreate.as_view(), name='new_group_view'),
    url(r'^group/(?P<pk>[0-9]+)/$', views.GroupDetail.as_view(), name='group_detail'),
    url(r'^group/(?P<pk>[0-9]+)/edit$', views.GroupEdit.as_view(), name='group_edit'),
    url(r'^new_group$', views.create_new_group, name='new_group'),

    url(r'^topic/all/$', views.TopicList.as_view(), name='topic_list_view'),
    url(r'^topic/new/$', views.TopicCreate.as_view(), name='new_topic_view'),
    url(r'^topic/(?P<pk>[0-9]+)/$', views.TopicDetail.as_view(), name='topic_detail'),
    url(r'^topic/(?P<pk>[0-9]+)/edit$', views.TopicEdit.as_view(), name='topic_edit'),
    url(r'^toggle-topic$', views.toggle_topic, name='toggle_topic'),

    url(r'^update_manager$', views.update_manager, name='update_manager'),

    # url(r'^admin/', include(admin.site.urls)),
]
