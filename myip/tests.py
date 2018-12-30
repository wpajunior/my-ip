from django.test import SimpleTestCase
from django.urls import reverse
import myip.views


class IndexViewContentTest(SimpleTestCase):
    def setUp(self):
        self.remote_ip = '10.10.10.10'
        self.response = self.client.get(reverse('myip:index'), REMOTE_ADDR=self.remote_ip)

    def test_never_caching_headers(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTrue(self.response.has_header('Cache-Control'))
        self.assertTrue('max-age=0' in self.response['Cache-Control'])
        self.assertTrue('no-cache' in self.response['Cache-Control'])
        self.assertTrue('no-store' in self.response['Cache-Control'])
        self.assertTrue('must-revalidate' in self.response['Cache-Control'])

    def test_display_remote_ip_in_title(self):
        html = self.response.content.decode('utf8')
        self.assertEqual(self.response.status_code, 200)
        self.assertRegex(html, '<title>.*{}.*</title>'.format(self.remote_ip))

    def test_display_remote_ip_in_body(self):
        html = self.response.content.decode('utf8')
        self.assertEqual(self.response.status_code, 200)
        self.assertRegex(html, '<body>(.|\n)*{}(.|\n)*</body>'.format(self.remote_ip))
    
    def test_display_hostname(self):
        remote_ip = '127.0.0.1'
        hostname = 'localhost'
        response = self.client.get(reverse('myip:index'), REMOTE_ADDR=remote_ip)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '({})'.format(hostname))


class ExternalFunctionsTest(SimpleTestCase):
    def test_get_hostname(self):
        self.assertEqual(myip.views.get_hostname('127.0.0.1'), 'localhost')
        self.assertEqual(myip.views.get_hostname('203.0.113.0'), '') # TEST_NET-3


class LangaguesSuportTest(SimpleTestCase):
    def test_language_support_english(self):
        response = self.client.get(reverse('myip:index'), HTTP_ACCEPT_LANGUAGE='en')
        self.assertEqual(response.status_code, 200)
        self.assertIn('My IP address is', response.content.decode('utf8'))
    
    def test_language_support_german(self):
        response = self.client.get(reverse('myip:index'), HTTP_ACCEPT_LANGUAGE='de')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Meine IP-Adresse ist', response.content.decode('utf8'))
         
    def test_language_support_spanish(self):
        response = self.client.get(reverse('myip:index'), HTTP_ACCEPT_LANGUAGE='es')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Mi dirección IP es', response.content.decode('utf8'))
    
    def test_language_support_portuguese(self):
        response = self.client.get(reverse('myip:index'), HTTP_ACCEPT_LANGUAGE='pt-BR')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Meu endereço IP é', response.content.decode('utf8'))