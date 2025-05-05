from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    puntos = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Visita(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.TextField(blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cliente.puntos += 1
        self.cliente.save()
