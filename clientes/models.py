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

    # Visión lejana
    esferico_od_lejana = models.CharField(max_length=10, blank=True)
    cilindrico_od_lejana = models.CharField(max_length=10, blank=True)
    eje_od_lejana = models.CharField(max_length=10, blank=True)

    esferico_oi_lejana = models.CharField(max_length=10, blank=True)
    cilindrico_oi_lejana = models.CharField(max_length=10, blank=True)
    eje_oi_lejana = models.CharField(max_length=10, blank=True)

    # Visión cercana
    esferico_od_cercana = models.CharField(max_length=10, blank=True)
    cilindrico_od_cercana = models.CharField(max_length=10, blank=True)
    eje_od_cercana = models.CharField(max_length=10, blank=True)

    esferico_oi_cercana = models.CharField(max_length=10, blank=True)
    cilindrico_oi_cercana = models.CharField(max_length=10, blank=True)
    eje_oi_cercana = models.CharField(max_length=10, blank=True)

    # Lentes de contacto
    esferico_od_contacto = models.CharField(max_length=10, blank=True)
    cilindrico_od_contacto = models.CharField(max_length=10, blank=True)
    eje_od_contacto = models.CharField(max_length=10, blank=True)

    esferico_oi_contacto = models.CharField(max_length=10, blank=True)
    cilindrico_oi_contacto = models.CharField(max_length=10, blank=True)
    eje_oi_contacto = models.CharField(max_length=10, blank=True)

    # Adición y observaciones
    adicion = models.CharField(max_length=100, blank=True)
    tipo_lente_contacto = models.CharField(max_length=100, blank=True)  # Ej. orgánico, blue light

    # Tipo de lente marcada
    monofocal = models.BooleanField(default=False)
    multifocal = models.BooleanField(default=False)
    bifocal = models.BooleanField(default=False)
    por_separado = models.BooleanField(default=False)
    organico = models.BooleanField(default=False)
    antirreflejo = models.BooleanField(default=False)
    uvx = models.BooleanField(default=False)
    fotocromatico = models.BooleanField(default=False)

    # Referencias y precios
    ref_armazon = models.CharField(max_length=100, blank=True)
    ref_cristal = models.CharField(max_length=100, blank=True)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    entrega = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Medidas adicionales
    dip = models.CharField(max_length=20, blank=True)
    naso_pupilar_od = models.CharField(max_length=20, blank=True)
    naso_pupilar_oi = models.CharField(max_length=20, blank=True)
    alt = models.CharField(max_length=20, blank=True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cliente.puntos += 1
        self.cliente.save()

    def __str__(self):
        return f"Visita de {self.cliente} - {self.fecha}"
