from django.test import TestCase, Client
from django.urls import reverse, resolve
from ebarber.models import Area, Customer, Barbershop
from ebarber.views import *
from django.test.client import RequestFactory

class TestViews(TestCase):

    # Set up method for facilitating the tests
    def setUp(self):
        self.index_url = reverse('ebarber:index')
        self.search_url = reverse('ebarber:search')


    #Test for index view

    def test_index_GET(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'ebarber/index.html')


    #Tests for search view

    def test_search_notSelectedArea(self):
        response = self.client.get(self.search_url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['message'], 'Please select an area ')


    def test_search_BarbershopDoesNotExists(self):
        # Creating a testing area
        test_area = Area.objects.create(
            id = 1,
            name = 'Kolonos'
        )
        # We are not creating a testing barbershop for the purpose of the test

        response = self.client.get(self.search_url, {'area': test_area.id})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['message'], 'There are no barbershops in this area yet ')


    def test_search_BarbershopDoExists(self):
        # Creating a testing area
        test_area = Area.objects.create(
            id = 1,
            name = 'Kolonos'
        )
        # Creating a testing barbershop
        test_barbershop = Barbershop.objects.create(
            id = 1,
            username = 'GoldClipp',
            password = '123456',
            email = 'goldclip@hotmail.com',
            phone = '2106647621',
            address = 'Golden 3',
            area = Area.objects.get(pk=test_area.id)
        )

        response = self.client.get(self.search_url, {'area': test_area.id})
        self.assertEquals(response.status_code, 200)
        self.assertTrue(len(response.context['availables']) > 0)
