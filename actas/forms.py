from django import forms
from actas.models import Acta, Foto
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from captcha.fields import ReCaptchaField

from actas.funciones import modificar_imagen

class ActaForm(forms.ModelForm):
    class Meta:
        model = Acta
        fields = ('titulo', 'descripcion', 'archivo', 'link', 'tags',)
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'input'}),
            'link': forms.TextInput(attrs={'class':'input'}),
            'descripcion': forms.Textarea(attrs={'class':'textarea'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'file-input', 'accept': '.pdf, .doc, .docx, .odt, .xml, application/msword, application/pdf, application/vnd.oasis.opendocument.text, application/vnd.openxmlformats-officedocument.wordprocessingml.document'}),
        }
    
    def clean(self):
        super(ActaForm, self).clean()
        link = self.cleaned_data.get('link')
        archivo = self.cleaned_data.get('archivo')
        if link and archivo:
            raise ValidationError(_('Puedes subir o un archivo o un enlance, no ambos'))
        if not link and not archivo:
            raise ValidationError(_('Debes subir al menos un tipo de recurso: o un archivo o un enlance'))

    def clean_archivo(self):
        data = self.cleaned_data['archivo']
        if data:
            if data.size > 5242880:
                raise ValidationError(_('El archivo no debe pesar más de 5 MB'))
        return data

class MailArchivo(forms.Form):
    nombre = forms.CharField(required=True, 
                             min_length=5, 
                             max_length=100,
                             widget=forms.TextInput(attrs={'class': 'input'}))

    correo = forms.EmailField(required=True,
                              widget=forms.EmailInput(attrs={'class': 'input'})) 

    descripcion = forms.CharField(required=True,
                                  max_length=500,
                                 label="Mensaje",
                                 widget=forms.Textarea(attrs={'class': 'textarea'}))

    archivo = forms.FileField(required=True,
                              help_text='El archivo no debe superar los 5 MB',
                              widget=forms.ClearableFileInput(attrs={'class': 'file-input', 'accept': '.pdf, .doc, .docx, .odt, .xml, application/msword, application/pdf, application/vnd.oasis.opendocument.text, application/vnd.openxmlformats-officedocument.wordprocessingml.document'}))

    captcha = ReCaptchaField()

    def clean_archivo(self):
        data = self.cleaned_data['archivo']
        if data.size > 5242880:
            raise ValidationError(_('El archivo no debe pesar más de 5 MB'))
        return data

class FotoForm(forms.ModelForm):
    class Meta:
        model = Foto
        fields = ('archivo', 'descripcion')
        widgets = {
            'descripcion': forms.Textarea(attrs={'class':'textarea'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'file-input', 'accept': 'image/*'}),
        }

    def clean_archivo(self):
        data = self.cleaned_data['archivo']
        imgfile = modificar_imagen(data)
        return imgfile
