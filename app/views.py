from django.shortcuts import get_object_or_404, redirect
from .models import Pizzas, Gaseosas_disponibles, Pizzas_dia, Compra, DetalleProducto
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType


def agregar_a_compra(request, producto_id):
    """
    Agrega un producto a la compra activa.

    Recibe el id del producto desde la url y la cantidad y el tipo desde el formulario.
    El 'tipo' debe ser 'pizza' o 'gaseosa'.
    """
    if request.method != 'POST':
        messages.error(request, 'Método no permitido.')
        return redirect('lista')

    tipo_producto_str = request.POST.get('tipo')
    cantidad = int(request.POST.get('cantidad', 1))
    
    modelo_producto = None
    if tipo_producto_str == 'pizza':
        modelo_producto = Pizzas
    elif tipo_producto_str == 'gaseosa':
        modelo_producto = Gaseosas_disponibles
    
    if not modelo_producto:
        messages.error(request, 'Tipo de producto no válido.')
        return redirect('lista')

    producto = get_object_or_404(modelo_producto, id=producto_id)
    
    # Asumo que el usuario logueado está en request.user
    compra, _ = Compra.objects.get_or_create(usuario=request.user, estado=True)

    content_type = ContentType.objects.get_for_model(producto)

    detalle_producto, created = DetalleProducto.objects.get_or_create(
        compra=compra,
        content_type=content_type,
        object_id=producto.id,
        defaults={'cantidad': 0}
    )

    nueva_cantidad_total = detalle_producto.cantidad + cantidad

    # Asumo que tus modelos de producto tienen un campo 'stock'
    if hasattr(producto, 'stock') and nueva_cantidad_total > producto.stock:
        messages.error(request, 'La cantidad solicitada excede el stock disponible')
        return redirect('lista')

    detalle_producto.cantidad = nueva_cantidad_total
    detalle_producto.save()

    compra.actualizar_total()

    return redirect('lista')


def eliminar_del_carrito(request, producto_id):
    """
    Elimina un producto del carrito.
    Recibe el id del producto desde la url y el 'tipo' desde el formulario (POST).
    """
    if request.method != 'POST':
        messages.error(request, 'Método no permitido.')
        return redirect('lista')

    tipo_producto_str = request.POST.get('tipo')
    modelo_producto = None
    if tipo_producto_str == 'pizza':
        modelo_producto = Pizzas
    elif tipo_producto_str == 'gaseosa':
        modelo_producto = Gaseosas_disponibles

    if not modelo_producto:
        messages.error(request, 'Tipo de producto no válido.')
        return redirect('lista')

    producto = get_object_or_404(modelo_producto, id=producto_id)
    compra = get_object_or_404(Compra, usuario=request.user, estado=True)
    content_type = ContentType.objects.get_for_model(producto)

    try:
        detalle_producto = DetalleProducto.objects.get(
            compra=compra,
            content_type=content_type,
            object_id=producto.id
        )
        detalle_producto.delete()
        compra.actualizar_total()
        messages.success(request, 'Producto eliminado del carrito.')
    except DetalleProducto.DoesNotExist:
        messages.error(request, 'Este producto no está en tu carrito.')
    
    return redirect('lista')


def cerrar_compra(request):
    """
    Cierra la compra actual y actualiza el stock de los productos.
    """    
    try:
        compra = Compra.objects.get(usuario=request.user, estado=True)
        detalles = DetalleProducto.objects.filter(compra=compra)
        
        if not detalles.exists():
            messages.error(request, 'No hay productos en el carrito para cerrar la compra.')
            return redirect('lista')

        for detalle in detalles:
            producto = detalle.producto  # Gracias a GenericForeignKey, esto funciona.
            if hasattr(producto, 'stock'): # Verificamos si el producto tiene stock
                producto.stock -= detalle.cantidad
                producto.save()

        compra.cerrar_compra()
        messages.success(request, '¡Compra realizada con éxito!')
        return redirect('lista')
    except Compra.DoesNotExist:
        messages.error(request, 'No hay una compra activa.')
        return redirect('lista')


def actualizar_cantidad(request, producto_id):
    """
    Actualiza la cantidad de un producto en el carrito.
    Recibe el id del producto de la url y la nueva cantidad y el tipo del formulario (POST).
    """
    if request.method != 'POST':
        messages.error(request, 'Método no permitido.')
        return redirect('lista')

    nueva_cantidad = int(request.POST.get('cantidad', 1))
    tipo_producto_str = request.POST.get('tipo')
    
    modelo_producto = None
    if tipo_producto_str == 'pizza':
        modelo_producto = Pizzas
    elif tipo_producto_str == 'gaseosa':
        modelo_producto = Gaseosas_disponibles

    if not modelo_producto:
        messages.error(request, 'Tipo de producto no válido.')
        return redirect('lista')

    producto = get_object_or_404(modelo_producto, id=producto_id)
    compra = get_object_or_404(Compra, usuario=request.user, estado=True)
    content_type = ContentType.objects.get_for_model(producto)

    try:
        detalle_producto = DetalleProducto.objects.get(
            compra=compra,
            content_type=content_type,
            object_id=producto.id
        )
        
        if nueva_cantidad <= 0:
            detalle_producto.delete()
            messages.info(request, 'Producto eliminado del carrito.')
        else:
            # Opcional: verificar stock antes de actualizar
            if hasattr(producto, 'stock') and nueva_cantidad > producto.stock:
                messages.error(request, 'La cantidad solicitada excede el stock disponible.')
            else:
                detalle_producto.cantidad = nueva_cantidad
                detalle_producto.save()
                messages.success(request, 'Cantidad actualizada.')
        
        compra.actualizar_total()

        except DetalleProducto.DoesNotExist:

            messages.error(request, 'Este producto no está en tu carrito para actualizar.')

    

        return redirect('lista')

    

    

    from django.shortcuts import render

    

    def lista_productos(request):

        """

        Muestra la lista de productos disponibles y el carrito de compras actual.

        """

        pizzas = Pizzas.objects.filter(disponible=True)

        gaseosas = Gaseosas_disponibles.objects.filter(disponible=True)

        

        compra_activa = None

        detalles_compra = []

        if request.user.is_authenticated:

            compra_activa, _ = Compra.objects.get_or_create(usuario=request.user, estado=True)

            detalles_compra = compra_activa.detalles.all()

    

        context = {

            'pizzas': pizzas,

            'gaseosas': gaseosas,

            'carrito': compra_activa,

            'detalles_carrito': detalles_compra,

        }

        return render(request, 'lista.html', context)

    