from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class ProductoBase(models.Model):
    """
    Clase base que sirve como plantilla a los demas productos

    """
    nombre = models.CharField(max_length=100, verbose_name="nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="precio")
    disponible = models.BooleanField(default=True, verbose_name="disponible")
    foto = models.ImageField(upload_to="productos", blank=True, null=True, verbose_name="foto")

    class Meta:
        abstract = True  ###  !No crea tabla en BD; solo sirve como base común¡

    def __str__(self):
        return self.nombre


class Pizzas(ProductoBase):
    """Esta clase hereda de producto base y unicamente requiere de el nombre y precio"""
    #nombre
    #precio




class Gaseosas_disponibles(ProductoBase):
    TIPO_CHOICES = [
        ('Personal', 'Personal'),
        ('1.5L', '1.5 Litros'),
        ('3L', '3 Litros'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)


    def actualizar_gaseosa():
    #ESTOY EN PROCESO DE AVERIGUAR COMO HACER ESTO


class Pizzas_dia(models.Model): 
    """Espera recibir el id de las pizzas existentes y la cantidad de pizzas que se van a sumar a la disponibilidad"""
    pizza = models.ForeignKey("Pizzas", related_name="pizzas_dia")
    #Aqui uso la disponibilidad de las pizzas es decir si esta activa o no... xd
    cantidad_disponible = models.IntegerField() 

    def actualizar_disponibilidad_pizza(self):
        """Actualiza la disponibilidad de la pizza"""
        if cantidad_disponible is 0:
            self.disponible = False 


        if cantidad_disponible > 0:
            self.disponible = True







class Compra(models.Model):     
    fecha = models.DateTimeField(auto_now_add=True)  
    total = models.DecimalField(max_digits=10, decimal_places=0, default=0) 
    estado = models.BooleanField(default=True)

    def __str__(self):         
        return f"Compra {self.id} - {self.order_date}" 

    def actualizar_total(self):
        """Esta funcion se encarga de actualizar el total de la compra por cliente"""
        self.total = sum(detalle.subtotal for detalle in self.detalles.all())  
        self.save()

    def cerrar_compra(self):  # Finaliza la compra 
        self.estado = False
        self.save()

        #IMPLEMENTAR GATILLO AL MOEMNTO DE CERRAR LA COMPRA PARA DESCONTAR LA GASEOSA DEL INVENTARIO Y LA PIZZA DE LAS DISPONIBLES.







class DetalleProducto(models.Model):
    """
    Clase que representa los ítems de la orden.
    """
    compra = models.ForeignKey(Compra, related_name='detalles', on_delete=models.CASCADE)  # Relación con la compra.
    cantidad = models.PositiveIntegerField()  # Cantidad del producto.
        
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    producto = GenericForeignKey('content_type', 'object_id')




    def __str__(self):
        return f"Detalle de compra {self.id} - {self.compra}"
    
    @property  # Permite acceder a este método como un atributo, sin necesidad de llamarlo como una función.
    def subtotal(self):  # Calcula el subtotal de cada producto en función de su cantidad.
        # Multiplica la cantidad del producto por su precio final para obtener el subtotal.
        return self.cantidad * self.producto.precio_final
