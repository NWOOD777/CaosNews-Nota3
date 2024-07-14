from django.db import models

class Categoria(models.Model):
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return self.descripcion

class Periodista(models.Model):
    rut = models.CharField(max_length=12)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    edad = models.IntegerField(default=0)
    telefono = models.CharField(max_length=20)
    correo = models.CharField(max_length=50)
    genero = models.CharField(max_length=20)
    imagen_perfil = models.ImageField(upload_to='noticias', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Noticia(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    periodista = models.ForeignKey(Periodista, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    habilitado = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='noticia', blank=True, null=True)

    def __str__(self):
        return self.titulo

class Pago(models.Model):
    nombre_usuario = models.CharField(max_length=100)
    email_usuario = models.EmailField()
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pago {self.transaction_id} de {self.customer_name}"
