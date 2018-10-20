from django.test import SimpleTestCase
from django.urls import reverse
import myip.views

class IndexViewTests(SimpleTestCase):
    def test_never_caching_headers(self):
        response = self.client.get(reverse('myip:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.has_header('Cache-Control'))
        self.assertTrue('max-age=0' in response['Cache-Control'])
        self.assertTrue('no-cache' in response['Cache-Control'])
        self.assertTrue('no-store' in response['Cache-Control'])
        self.assertTrue('must-revalidate' in response['Cache-Control'])

    def test_display_remote_ip_in_title(self):
        remote_ip = '10.10.10.10'
        response = self.client.get(reverse('myip:index'), REMOTE_ADDR=remote_ip)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertRegex(html, '<title>.*{}.*</title>'.format(remote_ip))

    def test_display_remote_ip_in_body(self):
        remote_ip = '10.10.10.10'
        response = self.client.get(reverse('myip:index'), REMOTE_ADDR=remote_ip)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertRegex(html, '<body>(.|\n)*{}(.|\n)*</body>'.format(remote_ip))
    
    def test_display_hostname(self):
        remote_ip = '127.0.0.1'
        hostname = 'localhost'
        response = self.client.get(reverse('myip:index'), REMOTE_ADDR=remote_ip)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '({})'.format(hostname))
    
    def test_get_hostname(self):
        self.assertEqual(myip.views.get_hostname('127.0.0.1'), 'localhost')
        self.assertEqual(myip.views.get_hostname('203.0.113.0'), '') # TEST_NET-3
    
    def test_language_support_english(self):
        response = self.client.get(reverse('myip:index'), HTTP_ACCEPT_LANGUAGE='en')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My IP address is')
    
    def test_language_support_german(self):
        response = self.client.get(reverse('myip:index'), HTTP_ACCEPT_LANGUAGE='de')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Meine IP-Adresse ist')
    
    def test_language_support_spanish(self):
        response = self.client.get(reverse('myip:index'), HTTP_ACCEPT_LANGUAGE='es')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mi dirección IP es')
    
    def test_language_support_portuguese(self):
        response = self.client.get(reverse('myip:index'), HTTP_ACCEPT_LANGUAGE='pt-BR')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Meu endereço IP é')
