from django.core.urlresolvers import resolve
from django.test import TestCase
from main.views import IndexView

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.view_name, 'home')
