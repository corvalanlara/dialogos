from django.test import TestCase

class HomePageTest(TestCase):

    def test_inicio_devuelve_el_html_correcto(self):
        respuesta = self.client.get('/')
        self.assertTemplateUsed(respuesta, 'index.html')
