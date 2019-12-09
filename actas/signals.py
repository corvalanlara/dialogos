from django.db.models.signals import post_save, post_delete
from django.contrib.auth import user_logged_in, user_login_failed, user_logged_out
from django.dispatch import receiver
from django.contrib.auth.models import User
import logging
from actas.models import Acta, Foto

log = logging.getLogger('cabildo.info')

@receiver(post_save, sender=Acta)
def acta_save_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        log.info(f'Dialogos: Nuevo documento creado {instance.titulo}, n° {instance.codigo}')
    else:
        log.info(f'Dialogos: Documento n° {instance.codigo} actualizado')

@receiver(post_save, sender=Foto)
def foto_save_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        log.info(f'Dialogos: Nueva fotografía subida n° {instance.id}')

@receiver(post_delete, sender=Acta)
def acta_delete_handler(sender, instance, using, **kwargs):
    log.info(f'Dialogos: El documento {instance.codigo} ha sido eliminado')

@receiver(post_delete, sender=Foto)
def foto_delete_handler(sender, instance, using, **kwargs):
    log.info(f'Dialogos: La fotografía {instance.id} ha sido eliminada')

@receiver(user_logged_in, sender=User)
def user_in_handler(sender, request, user, **kwargs):
    log.info(f'Dialogos: {user.username} ha ingresado a la página')

@receiver(user_logged_out, sender=User)
def user_out_handler(sender, request, user, **kwargs):
    log.info(f'Dialogos: {user.username} se ha desconectado')

@receiver(user_login_failed, sender=User)
def user_fail_handler(sender, credentials, request, **kwargs):
    log.info(f'Dialogos: Una persona ha intentado ingresar usando estas credenciales {credentials}')
