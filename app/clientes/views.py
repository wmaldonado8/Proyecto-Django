from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import FormularioCliente, FormularioCuenta, FormularioTransaccion, FormularioTransferencia
from app.modelo.models import Cliente, Cuenta,Transaccion, Transferencia
import random
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def principal(request):
    usuario = request.user
    print(usuario.get_all_permissions())
    if usuario.has_perm('modelo.view_cliente'):
        listaClientes = Cliente.objects.all().order_by('apellidos')
        context = {

            'title': "Clientes",
            'mensaje': "Clientes"
        }
        return render(request, 'clientes/home_cliente.html', context)
    else:
        messages.warning(request, 'No Permitido')
        return render(request, 'login/403.html')


     
@login_required
def buscar(request):
    usuario = request.user
    print(usuario.get_all_permissions())
    if usuario.has_perm('modelo.view_cliente'):
        dni = request.GET['txt_buscar']
        listaClientes = Cliente.objects.filter(cedula =dni)
        context = {
            'clientes': listaClientes,
            'title': "Lista Clientes",
            'mensaje': "Lista Clientes"
        }
        return render(request, 'clientes/home_cliente.html', context)
    else:
        messages.warning(request, 'No Permitido')
        return render(request, 'login/403.html')



@login_required()
def buscarCuenta(request):
    usuario = request.user
    print(usuario.get_all_permissions())
    if usuario.has_perm('modelo.view_cliente'):
        dni = request.GET['txt_buscarCuenta']
        cliente=Cliente.objects.get(cedula=dni)
        listaClientes = Cuenta.objects.filter(cliente=cliente)
        context = {

            'clientes': listaClientes,
            'title': "LISTA DE CUENTAS",
            'mensaje': "Modulo Clientes"
        }
        return render(request, 'clientes/home_cuenta.html', context)
    else:
        messages.warning(request, 'No permitido')
        return render(request,'login/403.html')



        


def principalCuenta(request):
    usuario = request.user
    print(usuario.get_all_permissions())
    if usuario.has_perm('modelo.view_cliente'):
        listaClientes = Cuenta.objects.all()
        context = {

            'title': "Cuentas",
            'mensaje': "Cuentas"
        }
        return render(request, 'clientes/home_cuenta.html', context)
    else:
        messages.warning(request, 'No Permitido')
        return render(request, 'login/403.html')



def saludar(request):
    return HttpResponse('Hola clase')

@login_required
def crear(request):
    usuario = request.user
    if usuario.has_perm('modelo.add_cliente'):
        formulario = FormularioCliente(request.POST)
        if request.method == 'POST':
            if formulario.is_valid():
                datos = formulario.cleaned_data
                cliente = Cliente()
                cliente.cedula = datos.get('cedula')
                cliente.nombres = datos.get('nombres')
                cliente.apellidos = datos.get('apellidos')
                cliente.genero = datos.get('genero')
                cliente.estadoCivil = datos.get('estadoCivil')
                cliente.fechaNacimiento = datos.get('fechaNacimiento')
                cliente.correo = datos.get('correo')
                cliente.telefono = datos.get('telefono')
                cliente.celular = datos.get('celular')
                cliente.direccion = datos.get('direccion')
                cliente.save()
                messages.warning(request, 'Guardado Exitosamente')
                return redirect(principal)
        numero = random.randrange(10)
        context = {
            'f': formulario,
            'title': "Ingresar Cliente",
            'mensaje': "Ingresar Nuevo Cliente"
        }
        return render(request, 'clientes/crear_cliente.html', context)
    else:
        messages.warning(request, 'No Permitido')
        return render(request, 'login/403.html')

@login_required
def modificar(request):
    usuario = request.user
    if usuario.has_perm('modelo.change_cliente'):
        dni = request.GET['cedula'];
        cliente = Cliente.objects.get(cedula=dni)
        formulario = FormularioCliente(instance=cliente)

        if request.method == 'POST':
            cliente.cedula = request.POST['cedula']
            cliente.apellidos = request.POST['apellidos']
            cliente.nombres = request.POST['nombres']
            cliente.genero = request.POST['genero']
            cliente.estadoCivil = request.POST['estadoCivil']
            cliente.fechaNacimiento = request.POST['fechaNacimiento']
            cliente.correo = request.POST['correo']
            cliente.telefono = request.POST['telefono']
            cliente.celular = request.POST['celular']
            cliente.direccion = request.POST['direccion']
            cliente.save()
            messages.warning(request, 'Datos Modificados')
            return redirect(principal)
        context = {
            'f': formulario,
            'title': "Modificar Cliente",
            'mensaje': "Modificar datos de " + cliente.nombres + " " + cliente.apellidos
        }
        return render(request, 'clientes/crear_cliente.html', context)
    else:
        messages.warning(request, 'No Permitido')
        return render(request, 'login/403.html')


@login_required
def eliminar(request):
    usuario = request.user
    if usuario.has_perm('modelo.delete_cliente'):
        dni = request.GET['cedula'];
        cliente = Cliente.objects.get(cedula=dni)
        if cliente:
            if cliente.delete():
                messages.warning(request, 'Cliente Eliminado')
            else:
                messages.warning(request, 'No se pudo Eliminar')
            return redirect(principal)
        else:
            messages.warning(request, 'Perdido')
            return redirect(principal)
        return render(request, 'clientes/crear_cliente.html', context)
    else:
        messages.warning(request, 'No Permitido')
        return render(request, 'login/403.html')

@login_required
def transaccion(request):
    usuario = request.user
    if usuario.has_perm('modelo.add_transaccion'):

        numero = request.GET['numero']
        cuenta=Cuenta.objects.get(numero=numero)
        formulario = FormularioTransaccion(request.POST)
        context = {
            'f': formulario,
            'numero': numero,
            'title': "Transaccion",
            'mensaje': "Ingresar Nueva Transaccion"
        }

        if request.method == 'POST':
            if formulario.is_valid():
                datos = formulario.cleaned_data
                transaccion = Transaccion()

                transaccion.cuenta = cuenta
                transaccion.tipo = datos.get('tipo')
                transaccion.valor = datos.get('valor')
                transaccion.descripcion = datos.get('descripcion')

                cuenta = Cuenta.objects.get(numero=numero)
                cuentaSuma = Cuenta.objects.filter(numero=numero)

                suma = 0

                for item in cuentaSuma:
                    if datos.get('tipo') == 'deposito':
                        suma = datos.get('valor')+ item.saldo
                    if datos.get('tipo') == 'retiro':
                        if item.saldo>= datos.get('valor'):
                            suma =  item.saldo - datos.get('valor')
                        else:
                            messages.warning(request, 'SALDO INSUFICIENTE')
                            return render(request, 'clientes/Transaccion.html', context)
                cuenta.saldo = suma;

                transaccion.save()
                cuenta.save()
                messages.warning(request, 'Guardado Exitosamente')
                context = {
                    'fecha': transaccion.fecha,
                    'tipo': transaccion.tipo,
                    'valor': transaccion.valor,
                    'cuenta': transaccion.cuenta,
                    'descripcion': transaccion.descripcion
                }
                return render(request, 'clientes/Presentar.html', context)
        numero = random.randrange(10)

        return render(request, 'clientes/Transaccion.html', context)
    else:
        messages.warning(request, 'No Permitido')
        return render(request, 'login/403.html')

@login_required
def crearCuenta(request):
    usuario = request.user
    if usuario.has_perm('modelo.change_cliente'):
        usuario = request.user
        if usuario.has_perm('modelo.add_cliente'):
            formulario = FormularioCuenta(request.POST)
            if request.method == 'POST':
                if formulario.is_valid():
                    numero = random.randint(1000000000,9999999999)
                    num = numero.__str__()
                    while Cuenta.objects.filter(numero = num).exists():
                        numero = random.randrange(10)

                    datos = formulario.cleaned_data
                    cuenta = Cuenta()
                    cuenta.numero = num
                    cuenta.saldo = "0"
                    cuenta.cliente = datos.get('cliente')
                    cuenta.tipoCuenta = datos.get('tipoCuenta')
                    cuenta.save()
                    messages.warning(request, 'Guardado Exitosamente')
                    return redirect(principalCuenta)
            context = {
                'f': formulario,
                'title': "Ingresar Cliente",
                'mensaje': "Ingresar Nuevo Cliente"
            }
            return render(request, 'clientes/crear_cliente.html', context)
        else:
            messages.warning(request, 'No Permitido')
            return render(request, 'login/403.html')


def buscarTrans(request):
    usuario = request.user
    if usuario.has_perm('modelo.view_cliente'):
        numero = request.GET['numero']
        context = {

            'title': "TRANSAFERENCIA",
            'cliente': numero,
            'permisoEditar': usuario.has_perm('modelo.change_cuenta'),
            'permisoCrear': usuario.has_perm('modelo.add_cuenta'),
        }

        return render(request, 'clientes/buscar.html', context)
    else:
        return redirect(principal)       




@login_required()
def verTransaccion(request):
    usuario = request.user
    if usuario.has_perm('modelo.add_cliente'):
        dni = request.GET['numero']
        c = Cuenta.objects.get(numero = dni)
        listaClientes = Transaccion.objects.filter(cuenta = c)
        context = {
            'title': "LISTA DE TRANSACCIONES DE: "+dni,
            'numero': dni,
            'lista' : listaClientes,
        }
        return render(request, 'clientes/ver_transaccion.html', context)
    else:
        messages.warning(request, 'No Permitido')
        return render(request, 'login/403.html')


@login_required
def crearTransferencia(request):
    usuario = request.user
    if usuario.has_perm('modelo.add_cliente'):
        numero = request.GET['numero']
        destino = request.GET['txt_buscar']
        context = {
            'title': "TRANSAFERENCIA",
            'cliente': numero,
            'permisoEditar': usuario.has_perm('modelo.change_cuenta'),
            'permisoCrear': usuario.has_perm('modelo.add_cuenta'),
        }
        try:
            cuenta2 = Cuenta.objects.get(numero=destino)
            cuenta1 = Cuenta.objects.get(numero = numero)
            if cuenta1==cuenta2:
                messages.warning(request, 'Cuenta Repetida')
                return render(request, 'clientes/buscar.html', context)
            formulario = FormularioTransferencia(request.POST)
            context = {
                'f': formulario,
                'cuenta1':cuenta1,
                'cuenta2': cuenta2,
                'title': "Ingresar Transaccion",
                'mensaje': "Ingresar Nueva Tranferencia"
            }
            if request.method == 'POST':
                if formulario.is_valid():
                    datos = formulario.cleaned_data
                    transferencia = Transferencia()
                    transferencia.cuenta1 = cuenta1
                    transferencia.cuenta2 = cuenta2
                    transferencia.valor = datos.get('valor')
                    transferencia.descripcion = datos.get('descripcion')

                    cuentaSuma = Cuenta.objects.filter(numero=numero)
                    suma = 0
                    for item in cuentaSuma:
                        if item.saldo >= datos.get('valor'):
                            suma = item.saldo - datos.get('valor')
                        else:
                            messages.warning(request, 'SALDO INSUFICIENTE')
                            return render(request, 'clientes/crear_Transferencia.html', context)
                    cuenta1.saldo = suma;

                    cuentaSuma2 = Cuenta.objects.filter(numero=destino)
                    for item in cuentaSuma2:
                        suma = item.saldo + datos.get('valor')
                    cuenta2.saldo = suma;

                    transferencia.save()
                    cuenta1.save()
                    cuenta2.save()
                    messages.warning(request, 'Guardado Exitosamente')
                    context = {
                        'fecha': transferencia.fecha,
                        'valor': transferencia.valor,
                        'cuenta1': transferencia.cuenta1,
                        'cuenta2': transferencia.cuenta2,
                        'descripcion': transferencia.descripcion
                    }
                    return render(request, 'clientes/Presentar_Transferencia.html', context)
        except :
            messages.warning(request, 'Cuenta Incorrecta')
            return render(request, 'clientes/buscar.html', context)

        numero = random.randrange(10)
        return render(request, 'clientes/crear_Transferencia.html', context)
    else:
        messages.warning(request, 'No Permitido')
        return render(request, 'login/403.html')
