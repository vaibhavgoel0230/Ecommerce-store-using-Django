from unittest import skip

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from store.models import Category, Product
from store.views import all_products

# @skip("demonstrating skipping")
# class TestSkip(TestCase):
#     def test_skip_example(self):
#         pass

class TestViewResponse(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='admin')
        self.data1 = Product.objects.create(category_id=1, title='mastering django',created_by_id=1,
                                        slug='mastering-django',price='20.00',image='django')

    def test_url_allowed_hosts(self):
        """
        Test Allowed Hosts
        """
        response = self.c.get('/')
        self.assertEqual(response.status_code,200)

    def test_product_detail_url(self):
        """
        Test Product response status
        """
        response = self.c.get(reverse('store:product_detail', args=['mastering-django']))
        self.assertEqual(response.status_code,200)

    def test_category_detail_url(self):
        """
        Test Category response status
        """
        response = self.c.get(reverse('store:category_list', args=['django']))
        self.assertEqual(response.status_code,200)

    def test_homepage_html(self):
        """
        Test Homepage html
        """
        request = HttpRequest()
        response = all_products(request)
        html = response.content.decode('utf8')
        self.assertIn('<div class="col">',html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code,200)

    def test_request_factory(self):
        request = self.factory.get('/item/mastering-django')
        response = all_products(request)
        html = response.content.decode('utf8')
        self.assertIn('<div class="col">',html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code,200)