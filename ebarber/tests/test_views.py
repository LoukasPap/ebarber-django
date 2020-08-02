from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from ebarber.models import Area, Customer, Barbershop
from ebarber.views import *

# Set up method to facilitate later testing
class TestViews(TestCase):

    # Set up method for facilitating the tests
    def setUp(self):
        self.test_area_obj = Area.objects.create(
            id = 1,
            name = 'Kolonos'
        )
        self.index_url = reverse('ebarber:index')
        self.search_url = reverse('ebarber:search')
        self.register_url = reverse('ebarber:register')

        self.test_area = {
            'id' : '1',
            'name' : Area.objects.get(pk=self.test_area_obj.id)
        }
        self.customer_user = {
            'kind' : 'customer',
            'username' : 'TestingC1',
            'password' : '123456',
            'email' : 'cus1@hotmail.com',
            'phone' : '6922222222',
            'name' : 'Adamantios',
            'surname' : 'Panagios'
        }
        self.customer_for_testing_existing_fields = {
            'kind' : 'customer',
            'username' : 'ExistingCustomer',
            'password' : '123456',
            'email' : 'anemail@hotmail.com',
            'phone' : '6922222222',
            'name' : 'Adamantios',
            'surname' : 'Panagios'
        }

        self.barbershop_user = {
            'kind' : 'barbershop',
            'username' : 'TestingB1',
            'password' : '123456',
            'email' : 'bar1@hotmail.com',
            'phone' : '6911111111',
            'address' : 'Street 44',
            'area' : self.test_area['id']
        }
        self.invalid_username = {
            'kind' : 'customer',
            'username' : 'Test',
            'password' : '123456',
            'email' : 'cus1@hotmail.com',
            'phone' : '6922222222',
            'name' : 'Adamantios',
            'surname' : 'Panagios'
        }
        self.invalid_password = {
            'kind' : 'customer',
            'username' : 'TesingC1t',
            'password' : '1234',
            'email' : 'cus1@hotmail.com',
            'phone' : '6922222222',
            'name' : 'Adamantios',
            'surname' : 'Panagios'
        }
        self.invalid_email = {
            'kind' : 'customer',
            'username' : 'TesingC1t',
            'password' : '123456',
            'email' : 'cus1.comr',
            'phone' : '6922222222',
            'name' : 'Adamantios',
            'surname' : 'Panagios'
        }
        self.invalid_phone = {
            'kind' : 'customer',
            'username' : 'TesingC1t',
            'password' : '123456',
            'email' : 'cus1@hotmail.comr',
            'phone' : '6922222',
            'name' : 'Adamantios',
            'surname' : 'Panagios'
        }
        self.customer_invalidName = {
        'kind' : 'customer',
        'username' : 'TestingC1',
        'password' : '123456',
        'email' : 'cus1@hotmail.com',
        'phone' : '6922222222',
        'name' : 'Adam',
        'surname' : 'Panagios'
        }
        self.customer_invalidSurname = {
        'kind' : 'customer',
        'username' : 'TestingC1',
        'password' : '123456',
        'email' : 'cus1@hotmail.com',
        'phone' : '6922222222',
        'name' : 'Adamantios',
        'surname' : 'Pan'
        }
        self.barbershop_invalidAddress = {
        'kind' : 'barbershop',
        'username' : 'TestingB1',
        'password' : '123456',
        'email' : 'bar1@hotmail.com',
        'phone' : '6911111111',
        'address' : 'A text to test the address field',
        'area' : self.test_area['id']
        }

#Tests for index and search view
class TestIndexAndSearch(TestViews):
    # Test for index view
    def test_index_page(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'ebarber/index.html')

    #Tests for search view
    def test_search_page(self):
        response = self.client.get(self.search_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'ebarber/index.html')

    def test_search_notSelectedArea(self):
        response = self.client.get(self.search_url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['message'], 'Please select an area ')

    def test_search_BarbershopDoesNotExists(self):
        response = self.client.get(self.search_url, {'area': self.test_area['id']})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['message'], 'There are no barbershops in this area yet ')

    def test_search_BarbershopDoExists(self):
        # Creating a testing barbershop
        test_barbershop = Barbershop.objects.create(
            id = 1,
            username = 'GoldClipp',
            password = '123456',
            email = 'goldclip@hotmail.com',
            phone = '2106647621',
            address = 'Golden 3',
            area = Area.objects.get(pk=self.test_area_obj.id)
        )

        response = self.client.get(self.search_url, {'area': self.test_area['id']})
        self.assertEquals(response.status_code, 200)
        self.assertTrue(len(response.context['availables']) > 0)

#Tests for register view
class TestRegister(TestViews):
    def test_register_customerSuccess(self):
        response=self.client.post(self.register_url, self.customer_user, format='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['success'], 'Your registration was successfull!')

    def test_register_barbershop_Success(self):
        response=self.client.post(self.register_url, self.barbershop_user, format='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.context['success'], 'Your registration was successfull!')

    def test_register_invalidUsername_LessThan5Characters(self):
        response=self.client.post(self.register_url, self.invalid_username, format='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['rcError'], '<ol><li>Username must be 5-25 characters long, and not contain numbers.</li></ol>')

    def test_register_invalidPassword_LessThan5Characters(self):
        response=self.client.post(self.register_url, self.invalid_password, format='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['rcError'], '<ol><li>Password must be 5-25 characters long.</li></ol>')

    def test_register_invalidEmail(self):
        response=self.client.post(self.register_url, self.invalid_email, format='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['rcError'], '<ol><li>Enter a valid e-mail.</li></ol>')

    def test_register_invalidPhone(self):
        response=self.client.post(self.register_url, self.invalid_phone, format='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['rcError'], '<ol><li>Phone must start with 69, 21 or 22 and be 10 digits long.</li></ol>')

    def test_register_customer_invalidName(self):
        response=self.client.post(self.register_url, self.customer_invalidName, format='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['rcError'], "<ol><li>Write your name from 5 to 25 characters and don't put numbers in it.</li></ol>")

    def test_register_customer_invalidSurname(self):
        response=self.client.post(self.register_url, self.customer_invalidSurname, format='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['rcError'], "<ol><li>Write your surname from 5 to 25 characters and don't put numbers in it.</li></ol>")

    def test_register_barbershop_invalidAddress(self):
        response=self.client.post(self.register_url, self.barbershop_invalidAddress, format='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['rbError'], "<ol><li>Write your address with no more than 25 characters.</li></ol>")

    def test_register_UsernameAndEmailExists(self):
        test_existing_username_and_email = Customer.objects.create(
            id = 1,
            username = 'ExistingCustomer',
            password = '123456',
            email = 'anemail@hotmail.com',
            phone = '6922222222',
            name = 'George',
            surname = 'Kruss'
        )
        response=self.client.post(self.register_url, self.customer_for_testing_existing_fields, format='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], 'Username and email already exist!')

    def test_register_UsernameExists(self):
        test_existing_username = Customer.objects.create(
            id = 1,
            username = 'ExistingCustomer',
            password = '123456',
            email = 'otheremail@hotmail.com',
            phone = '6922222222',
            name = 'George',
            surname = 'Kruss'
        )
        response=self.client.post(self.register_url, self.customer_for_testing_existing_fields, format='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], 'Username already exists! Try another. ')

    def test_register_EmailExists(self):
        test_existing_email = Customer.objects.create(
            id = 1,
            username = 'NotExistingCustomer',
            password = '123456',
            email = 'anemail@hotmail.com',
            phone = '6922222222',
            name = 'George',
            surname = 'Kruss'
        )
        response=self.client.post(self.register_url, self.customer_for_testing_existing_fields, format='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], 'Email already exists! Try another. ')
