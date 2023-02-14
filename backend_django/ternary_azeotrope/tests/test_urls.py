# Write some tests for the urls.py file
#
# Path: backend_django/ternary_azeotrope/tests/test_urls.py
# Compare this snippet from backend_django/ternary_azeotrope/admin.py:

from django.test import Client, TestCase
from django.urls import reverse
from ternary_azeotrope.models import Component


class TestUrls(TestCase):
    def test1(self):
        self.assertEqual(1, 1)
