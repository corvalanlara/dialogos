from django.db import models
import uuid
from django.utils.timezone import now
from taggit.managers import TaggableManager
from urllib.parse import urlparse

class Acta(models.Model):
    codigo = models.AutoField(primary_key=True)
    fecha_subida = models.DateTimeField(default=now)
    titulo = models.CharField(max_length=250)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='documentos/', help_text='Máximo 5MB', null=True, blank=True)
    link = models.URLField(blank=True)
    tags = TaggableManager(help_text="Separar tags con comas")

    @property
    def youtube(self):
        if self.link:
            hostname = urlparse(self.link).hostname
            if 'www.youtube.com' in hostname:
                codigo = urlparse(self.link).query.replace('v=', '')
                return f'https://www.youtube.com/embed/{codigo}'
            elif 'youtu.be' in hostname:
                codigo = urlparse(self.link).path.replace('/', '')
                return f'https://www.youtube.com/embed/{codigo}'
            else:
                return False
        return False

class Foto(models.Model):
    archivo = models.ImageField(upload_to='documentos/')
    descripcion = models.TextField(help_text="Descripción de lo que está ocurriendo en la imagen. Necesario para ser inclusivo con los estudiantes con visión limitada")
