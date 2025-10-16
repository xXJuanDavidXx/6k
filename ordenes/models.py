from django.db import models
#from app.models import Product #Se debe importar para los detalles de la orden.
from django.contrib.auth.models import User

# Create your models here.

class Order(models.Model):
    is_active = models.BooleanField(default=True) #Determina si la orden esta activa y no fue atendida
    order_date = models.DateTimeField(auto_now_add=True) #Se crea con la fecha actual 
    referencia = models.CharField()

    #Le estamos agregando un formato a la forma en la que se va representar en el admin.
    def __str__(self):
        return f"order {self.id} by {self.user}"



#En esta clase se guardan todos los items de la orden.
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE) #LLave foranea de Order
    product = models.ForeignKey(Product, on_delete=models.PROTECT) #Llave foranea de la clase products de la app principal (se importa) y en on_delete Protect para que no se borren los productos que ya estan en una orden 
    quantity = models.IntegerField() #Para la cantidad de productos elegida.


    def __str__(self) -> str:
        return f"{self.order} - {self.product}"



