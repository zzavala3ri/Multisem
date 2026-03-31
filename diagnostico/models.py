from django.db import models

class DiagnosticoGenerador(models.Model):

    OPCIONES = [
        ('bueno', 'Bueno'),
        ('regular', 'Regular'),
        ('malo', 'Malo'),
    ]

    SI_NO = [
        ('si', 'Sí'),
        ('no', 'No'),
    ]

    marca = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    tecnico = models.CharField(max_length=100)

    placas = models.CharField(max_length=2, choices=SI_NO)
    nivel_aceite = models.CharField(max_length=10, choices=OPCIONES)

    ruido = models.TextField()
    horometro = models.FloatField()

    enfriamiento = models.CharField(max_length=2, choices=SI_NO)
    fecha_prueba = models.DateTimeField(auto_now_add=True)

    estructura = models.CharField(max_length=10, choices=OPCIONES)
    oxidacion = models.TextField()

    cableado = models.CharField(max_length=10, choices=OPCIONES)
    tablero = models.CharField(max_length=10, choices=OPCIONES)

    aceite = models.CharField(max_length=10, choices=OPCIONES)
    filtro_aceite = models.CharField(max_length=10, choices=OPCIONES)
    filtro_aire = models.CharField(max_length=10, choices=OPCIONES)
    filtro_combustible = models.CharField(max_length=10, choices=OPCIONES)

    escape = models.CharField(max_length=10, choices=OPCIONES)
    bateria = models.CharField(max_length=10, choices=OPCIONES)

    arranca = models.CharField(max_length=2, choices=SI_NO)

    foto = models.ImageField(upload_to='paneles/', null=True, blank=True)

    creado = models.DateTimeField(auto_now_add=True)
    informacion_extra = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Diagnóstico {self.id}"