from django.db import models

# Create your models here.
"""
Modelo de Cliente que posee cuentas
"""
class Cliente(models.Model):

    listaGenero = (
        ('f', 'Femenino'),
        ('m', 'Masculino'),
    )
    listaEstadoCivil = (
        ('soltero', 'Solter@'),
        ('casado', 'Casad@'),
        ('viudo', 'Viud@'),
        ('divorciado', 'Divorciad@'),
        ('unionLibre', 'Unión Libre'),
    )

    cliente_id = models.AutoField(primary_key=True)
    cedula = models.CharField(unique=True, max_length=10, null = False)
    nombres = models.CharField(max_length=70, null = False)
    apellidos = models.CharField(max_length=70, null = False)
    genero = models.CharField(max_length=15,default="",choices = listaGenero, null = False)
    estadoCivil = models.CharField(max_length=15, default="",choices = listaEstadoCivil, null = False)
    fechaNacimiento = models.DateField(auto_now = False, auto_now_add = False, null = False)
    correo = models.EmailField(unique=True, max_length=100, null = False)
    telefono = models.CharField(max_length=15, null = False)
    celular = models.CharField(max_length=15, null = False)
    direccion = models.TextField(null = False)
    #uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.cedula
"""
modelo de Informacion del Banco
"""
class Banco(models.Model):

    nombre = models.CharField(primary_key=True, max_length=25)
    direccion = models.CharField(max_length=225)
    telefono = models.CharField(max_length=10)
    correo = models.EmailField(max_length=200)
"""
Modelo de Cuenta que se relaciona con cliente
"""
class Cuenta(models.Model):

    listaTipo = (
        ('corriente', 'Corriente'),
        ('ahorros', 'Ahorro'),
    
    )
    cuenta_id = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=20, unique=True, null = False)
    estado = models.BooleanField(null = False, default = True)
    fechaApertura = models.DateField(auto_now_add = True, null = False)
    saldo = models.DecimalField(max_digits=10, decimal_places=3, null = False)
    tipoCuenta = models.CharField(max_length=30, default='',choices = listaTipo, null = False)
    cliente = models.ForeignKey(
        'Cliente',
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.numero
"""
Modelo de Transaccion, en una cuenta se realizan varias transacciones de todo tipo
estas tienen un responsable, que puede ser un/a cajer@, trnasferencia online
o uso del servicio de cajero automatico
"""
class Transaccion(models.Model):

    listaTipoC = (
        ('retiro', 'Retiro'),
        ('deposito', 'Depósito'),
        ('transferencia', 'Transferencia'),
        ('prestamo', 'Pago de Prestamo'),
        ('nomina', 'Pagos de Nómina'),
        ('pensiones', 'Pagos de Pensiones'),
        ('dividendos', 'Dividendos'),
        ('reembolsoGastos', 'Reembolso de Gastos'),
        ('pagoProveedores', 'Reembolso de Gastos'),
        ('transferencia', 'Traslado de efectivo entre entidades bancarias'),
        ('seguros', 'Pago de Seguros'),
        ('iess', 'Pago del IESS'),
        ('hipotecas', 'Pago de Hipotecas'),
        ('serviciosBasico', 'Pago de Servicios Básicos'),
        ('tvCable', 'Cuentas de televisión por cable'),
        ('celular', 'Cuentas de celular'),
        ('online', 'Compras por Internet'),
        ('administracion', 'Servicio de Administración'),
        ('futuros', 'Pagos Futuros'),
    )
    transaccion_id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add = True, null = False)
    tipo = models.CharField(max_length=30, choices = listaTipoC, null = False)
    valor = models.DecimalField(max_digits=10, decimal_places=3, null = False)
    descripcion = models.TextField(null = False)
    cuenta = models.ForeignKey(
        'Cuenta',
        on_delete=models.CASCADE,
    )

class Transferencia(models.Model):

    transferencia_id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add = True, null = False)
    valor = models.DecimalField(max_digits=10, decimal_places=3, null = False)
    descripcion = models.TextField(null = False)
    cuenta1 = models.ForeignKey(
        'Cuenta',
        related_name='cuenta1',
        on_delete=models.CASCADE,
    )
    cuenta2 = models.ForeignKey(
        'Cuenta',
        related_name='cuenta2',
        on_delete=models.CASCADE,
    )





"""
modelo donde se registra la informacion de una transferencia online
"""
class BancaVirtual (models.Model):
    bancaVirtual_id = models.AutoField(primary_key=True)
    numeroCuentaDestino = models.CharField(max_length=20, unique=True, null = False)
    dniTitularCuentaDestino = models.CharField(unique=True, max_length=10, null = False)
    titularCuentaDestino = models.CharField(max_length=160, null = False)
    transaccion = models.ForeignKey(
        'Transaccion',
        on_delete=models.CASCADE,
    )
"""
modelo donde se registra los datos del cajer@ que realiza la transaccion
"""
class Caja (models.Model):
    caja_id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=70, null = False)
    apellidos = models.CharField(max_length=70, null = False)
    transaccion = models.ForeignKey(
        'Transaccion',
        on_delete=models.CASCADE,
    )
"""
modelo donde se registra la informacion del cajero automatico en el que se realiza una transaccion
"""
class CajeroAutomatico (models.Model):
    cajeroAutomatico_id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=15, null = False)
    ubicacion = models.TextField(null = False)
    transaccion = models.ForeignKey(
        'Transaccion',
        on_delete=models.CASCADE,
    )

