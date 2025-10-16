from django.db import models

# Create your models here.


class Inventario_Cierre(models.Model):
    insumo = models.CharField(max_lenght=100, null=False)
    unidades = models.CharField(max_lenght=100)
    gramos = models.CharField(max_lenght=100)



