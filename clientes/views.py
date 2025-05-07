# Ver detalle de un cliente específico
from django.utils.decorators import method_decorator


def cliente_detalle(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    visitas = Visita.objects.filter(cliente=cliente).order_by('-fecha')

    numero = cliente.telefono.replace("+", "").replace(" ", "")
    mensaje = f"Hola {cliente.nombre}, ¡gracias por confiar en nosotros!"
    cliente.whatsapp_link = f"https://wa.me/595{numero}?text={mensaje.replace(' ', '+')}"

    return render(request, 'clientes/cliente_detalle.html', {
        'cliente': cliente,
        'visitas': visitas
    })
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Cliente, Visita

@login_required
def dashboard(request):
    total_clientes = Cliente.objects.count()
    total_visitas = Visita.objects.count()
    clientes_con_beneficios = Cliente.objects.filter(puntos__gte=3).count()
    clientes = Cliente.objects.all()

    return render(request, 'clientes/dashboard.html', {
        'total_clientes': total_clientes,
        'total_visitas': total_visitas,
        'clientes_con_beneficios': clientes_con_beneficios,
        'clientes': clientes,
    })


# Vista para mostrar clientes con beneficios
@login_required
def clientes_con_beneficios(request):
    clientes = Cliente.objects.filter(puntos__gte=3)
    for cliente in clientes:
        numero = cliente.telefono.replace("+", "").replace(" ", "")
        mensaje = f"Hola {cliente.nombre}, ¡tenés beneficios disponibles en tu próxima visita!"
        cliente.whatsapp_link = f"https://wa.me/595{numero}?text={mensaje.replace(' ', '+')}"
    return render(request, 'clientes/clientes_con_beneficios.html', {'clientes': clientes})

@login_required
@csrf_exempt
def registrar_visita_rapida(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')

        cliente = get_object_or_404(Cliente, pk=cliente_id)

        # Campos de receta oftalmológica
        campos = [
            'esferico_od_lejana', 'cilindrico_od_lejana', 'eje_od_lejana',
            'esferico_oi_lejana', 'cilindrico_oi_lejana', 'eje_oi_lejana',
            'esferico_od_cercana', 'cilindrico_od_cercana', 'eje_od_cercana',
            'esferico_oi_cercana', 'cilindrico_oi_cercana', 'eje_oi_cercana',
            'esferico_od_contacto', 'cilindrico_od_contacto', 'eje_od_contacto',
            'esferico_oi_contacto', 'cilindrico_oi_contacto', 'eje_oi_contacto',
            'adicion', 'tipo_lente_contacto',
            'ref_armazon', 'ref_cristal',
            'dip', 'naso_pupilar_od', 'naso_pupilar_oi', 'alt',
        ]

        data = {campo: request.POST.get(campo, '') for campo in campos}
        try:
            total_venta = float(request.POST.get('total_venta') or 0)
            entrega = float(request.POST.get('entrega') or 0)
            saldo = float(request.POST.get('saldo') or 0)
        except ValueError:
            messages.error(request, 'Uno o más valores numéricos son inválidos.')
            return redirect('dashboard')

        # Campos numéricos adicionales
        try:
            total_venta = float(request.POST.get('total_venta', 0))
            entrega = float(request.POST.get('entrega', 0))
            saldo = float(request.POST.get('saldo', 0))
        except ValueError:
            messages.error(request, 'Uno o más campos numéricos son inválidos.')
            return redirect('dashboard')

        # Campos booleanos (checkboxes)
        bool_campos = ['monofocal', 'multifocal', 'bifocal', 'por_separado', 'organico', 'antirreflejo', 'uvx', 'fotocromatico']
        bool_data = {campo: request.POST.get(campo) == 'on' for campo in bool_campos}

        # Crear la visita con todos los datos
        Visita.objects.create(
            cliente=cliente,
            total_venta=total_venta,
            entrega=entrega,
            saldo=saldo,
            **data,
            **bool_data
        )

        messages.success(request, 'Visita registrada correctamente.')

    return redirect('dashboard')

# Ver lista de clientes
@login_required
def clientes_lista(request):
    clientes = Cliente.objects.all().order_by('apellido', 'nombre')
    return render(request, 'clientes/clientes_lista.html', {'clientes': clientes})

# Crear nuevo cliente
@login_required
def clientes_nuevo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '')
        apellido = request.POST.get('apellido', '')
        telefono = request.POST.get('telefono', '')
        email = request.POST.get('email', '')
        fecha_nacimiento = request.POST.get('fecha_nacimiento') or None

        if not nombre or not apellido or not telefono:
            messages.error(request, 'Nombre, apellido y teléfono son obligatorios.')
            return redirect('clientes_nuevo')

        Cliente.objects.create(
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            email=email,
            fecha_nacimiento=fecha_nacimiento
        )
        messages.success(request, 'Cliente registrado exitosamente.')
        return redirect('clientes_lista')

    return render(request, 'clientes/clientes_nuevo.html')

# Lista de visitas
@login_required
def visitas_lista(request):
    visitas = Visita.objects.select_related('cliente').order_by('-fecha')
    return render(request, 'clientes/visitas_lista.html', {'visitas': visitas})

@login_required
def detalle_visita(request, visita_id):
    visita = get_object_or_404(Visita, id=visita_id)
    return render(request, 'clientes/visitas_detalle.html', {'visita': visita})



# Vista para editar los datos de un cliente
@login_required
def cliente_editar(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)

    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre', cliente.nombre)
        cliente.apellido = request.POST.get('apellido', cliente.apellido)
        cliente.telefono = request.POST.get('telefono', cliente.telefono)
        cliente.email = request.POST.get('email', cliente.email)
        cliente.fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
        cliente.save()

        messages.success(request, 'Datos del cliente actualizados correctamente.')
        return redirect('cliente_detalle', cliente_id=cliente.id)

    return render(request, 'clientes/cliente_editar.html', {'cliente': cliente})
@login_required
@csrf_exempt
def cliente_eliminar(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)

    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente.')
        return redirect('clientes_lista')

    return render(request, 'clientes/cliente_confirmar_eliminar.html', {'cliente': cliente})
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Credenciales inválidas.")
    
    return render(request, 'login.html')

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def crear_superusuario(request):
    if request.method == "POST":
        User.objects.create_superuser(
            username=request.POST["username"],
            email=request.POST["email"],
            password=request.POST["password"]
        )
        return redirect("dashboard")  # o donde quieras
    return render(request, "clientes/crear_superuser.html")


def setup_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        User.objects.create_superuser(username=username, email=email, password=password)
        return redirect('login')

    return render(request, 'clientes/crear_superuser.html')