from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import hashlib

def modificar_imagen(data):
    nombre_real = data.file.name
    md5 = hashlib.md5()
    md5.update(repr(nombre_real).encode('utf-8'))
    nombre_random = md5.hexdigest()
    imgfile = BytesIO(data.read())
    img = Image.open(imgfile)
    w, h = img.size
    img = img.resize((w//4, h//4), Image.ANTIALIAS)
    imgfile = BytesIO()
    if 'exif' in img.info.keys():
        imgexif = img.info['exif']
        img.save(imgfile, format='JPEG', quality=40, optimize=True, exif=imgexif)
    else:
        img.save(imgfile, format='JPEG', quality=40, optimize=True)
    img_name = f'{nombre_random}.jpeg'
    imagen = ContentFile(imgfile.getvalue(), img_name)
    return imagen

def pedazos(lista, numero):
    for i in range(0, len(lista), numero):
        yield lista[i:i+numero]
