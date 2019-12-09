from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from taggit.models import Tag
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage, BadHeaderError

from actas.models import Acta, Foto
from actas.forms import ActaForm, MailArchivo, FotoForm
from actas.funciones import pedazos

from cabil.settings import DEFAULT_FROM_EMAIL

class Inicio(ListView):
    model = Acta
    context_object_name = 'documentos'
    template_name= 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Inicio, self).get_context_data(**kwargs)
        context['tags'] = Acta.tags.all()
        context['fotos'] = list(pedazos(Foto.objects.all(), 3))
        return context

class SubirFoto(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Foto
    template_name = 'subir_foto.html'
    form_class = FotoForm
    success_url = reverse_lazy('inicio')
    success_message = 'La fotografía ha sido publicada exitosamente'

class CrearActa(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Acta
    template_name = 'crear_acta.html'
    form_class = ActaForm
    success_url = reverse_lazy('inicio')
    success_message = 'El documento "%(titulo)s" ha sido publicado con éxito'

    def get_context_data(self, **kwargs):
        context = super(CrearActa, self).get_context_data(**kwargs)
        context['tags'] = Acta.tags.all()
        return context

class UpdateActa(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Acta
    form_class = ActaForm
    template_name = 'update_acta.html'
    success_url = reverse_lazy('inicio')
    success_message = 'El documento %(titulo)s fue actualizado con éxito'

@require_POST
def BorrarActa(request, pk):
    query = Acta.objects.get(pk=pk)
    query.archivo.delete(save=False)
    query.delete()
    messages.success(request, f'Has eliminado el documento {query.titulo}')
    return redirect('inicio')

@require_POST
def BorrarFoto(request, pk):
    query = Foto.objects.get(pk=pk)
    query.archivo.delete(save=False)
    query.delete()
    messages.success(request, f'Has eliminado una fotografía exitosamente')
    return redirect('inicio')

def EnviarMail(request):
    if request.method == 'POST':
        form = MailArchivo(request.POST, request.FILES)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            archivo = form.cleaned_data['archivo']
            try:
                msg = EmailMessage(
                    subject=f'Correo de {nombre} <{correo}>',
                    body = descripcion,
                    from_email = DEFAULT_FROM_EMAIL,
                    to = [DEFAULT_FROM_EMAIL,],
                    reply_to=[correo,],
                )
                msg.attach(archivo.name, archivo.read(), archivo.content_type)
                msg.send()
            except BadHeaderError:
                messages.error(request, f'Hubo un error durante el envío del correo')
                return HttpResponseRedirect(reverse('inicio'))
            messages.success(request, f'El correo se ha enviado exitosamente')
            return HttpResponseRedirect(reverse('inicio'))
    else:
        form = MailArchivo()

    return render(request, 'correo_archivo.html', {'form': form})
