from django.test import TestCase
from django.urls import reverse


class IndexTestCase(TestCase):
    def test_index_view_success(self):
        response = self.client.post(reverse('index'), {'city': 'New York'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertIn('current_temperature', response.context)
        self.assertIn('current_apparent_temperature', response.context)

    def test_index_view_get_request(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
