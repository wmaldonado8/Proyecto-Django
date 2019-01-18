from django.contrib import admin

# Register your models here.
from .models import Cliente
from .models import Banco
from .models import Cuenta
from .models import Transaccion
from .models import Transferencia
from .models import BancaVirtual
from .models import Caja
from .models import CajeroAutomatico

class AdminCliente(admin.ModelAdmin):

    list_display = ["cedula", "nombres", "apellidos", "genero", "estadoCivil", "fechaNacimiento", "correo", "telefono", "celular", "direccion"]
    list_editable = ["apellidos", "nombres", "genero"]
    list_filter = ["genero", "direccion", "fechaNacimiento", "estadoCivil"]
    search_fields = ["cedula", "nombres", "apellidos"]

    class Meta:
        model = Cliente

admin.site.register(Cliente, AdminCliente)

class AdminBanco(admin.ModelAdmin):
    list_display = ["nombre", "direccion", "telefono", "correo"]
    list_editable = ["direccion", "telefono", "correo"]
    list_filter = ["direccion"]
    search_fields = ["nombre", "correo"]

    class Meta:
        model = Banco

admin.site.register(Banco, AdminBanco)

class AdminCuenta(admin.ModelAdmin):

    list_display = ["numero", "estado", "fechaApertura", "saldo", "tipoCuenta", "cliente"]
    list_filter = ["fechaApertura", "estado", "tipoCuenta"]
    search_fields = ["numero", "cliente"]

    class Meta:
        model = Cuenta

admin.site.register(Cuenta, AdminCuenta)

class AdminTransaccion(admin.ModelAdmin):

    list_display = ["transaccion_id","fecha", "tipo", "valor", "descripcion", "cuenta"]
    list_filter = ["tipo"]
    search_fields = ["cuenta", "descripcion"]

    class Meta:
        model = Transaccion

admin.site.register(Transaccion, AdminTransaccion)

class AdminTransferencia(admin.ModelAdmin):

    list_display = ["transferencia_id","fecha", "valor", "descripcion", "cuenta1", "cuenta2"]
    search_fields = ["cuenta1","cuenta2" "descripcion"]

    class Meta:
        model = Transferencia

admin.site.register(Transferencia, AdminTransferencia)

class AdminBancaVirtual(admin.ModelAdmin):

    list_display = ["numeroCuentaDestino", "dniTitularCuentaDestino", "titularCuentaDestino", "transaccion"]
    list_filter = ["transaccion"]
    search_fields = ["titularCuentaDestino", "dniTitularCuentaDestino", "numeroCuentaDestino"]

    class Meta:
        model = BancaVirtual

admin.site.register(BancaVirtual, AdminBancaVirtual)

class AdminCaja(admin.ModelAdmin):

    list_display = ["nombres", "apellidos", "transaccion"]
    list_filter = ["transaccion"]
    search_fields = ["nombres", "apellidos"]

    class Meta:
        model = Caja

admin.site.register(Caja, AdminCaja)

class AdminCajeroAutomatico(admin.ModelAdmin):

    list_display = ["codigo", "ubicacion", "transaccion"]
    list_filter = ["transaccion"]
    search_fields = ["codigo", "ubicacion"]

    class Meta:
        model = CajeroAutomatico

admin.site.register(CajeroAutomatico, AdminCajeroAutomatico)
