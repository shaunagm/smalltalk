from django.conf.urls import url

from main import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='home'),
    # url(r'^admin/', include(admin.site.urls)),
]
