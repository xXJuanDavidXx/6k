from django.db import models

# Create your models here.


class inv_base(models.Model):
    """Base de inventario."""
    insumo = models.CharField(max_lenght=100, null=False)
    unidades = models.CharField(max_lenght=100)
    gramos = models.CharField(max_lenght=100)
    ml = models.CharField(max_lenght=100)


    def Descontar():
        """Se va a encargar de descontar de los insumos"""

