from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ebarber.views import index, search, bprof, register, login, logout

class TestUrls(SimpleTestCase):

    #Test index url
    def test_index_url_resolves(self):
        url = reverse('ebarber:index')
        self.assertEquals(resolve(url).func, index)

    #Test search url
    def test_search_url_resolves(self):
        url = reverse('ebarber:search')
        self.assertEquals(resolve(url).func, search)

    #Test bprof url
    def test_bprof_url_resolves(self):
        url = reverse('ebarber:bprof')
        self.assertEquals(resolve(url).func,bprof)

    #Test register url
    def test_register_url_resolves(self):
        url = reverse('ebarber:register')
        self.assertEquals(resolve(url).func, register)

    #Test login url
    def test_login_url_resolves(self):
        url = reverse('ebarber:login')
        self.assertEquals(resolve(url).func, login)

    #Test logout url
    def test_logout_url_resolves(self):
        url = reverse('ebarber:logout')
        self.assertEquals(resolve(url).func, logout)
