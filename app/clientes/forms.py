from django import forms
from app.modelo.models import Cliente
from app.modelo.models import Cuenta
from app.modelo.models import Banco
from app.modelo.models import Transaccion
from app.modelo.models import BancaVirtual
from app.modelo.models import Caja
from app.modelo.models import CajeroAutomatico, Transferencia

class FormularioCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["cedula", "nombres", "apellidos", "genero", "estadoCivil", "fechaNacimiento", "correo", "telefono", "celular", "direccion"]

class FormularioBanco(forms.ModelForm):
    class Meta:
        model = Banco
        fields = ["nombre", "direccion", "telefono", "correo"]

class FormularioCuenta(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = [ "cliente", "tipoCuenta"]

class FormularioTransaccion(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ["tipo", "valor", "descripcion"]


class FormularioTransferencia(forms.ModelForm):
    class Meta:
        model = Transferencia
        fields = ["valor", "descripcion"]


class FormularioBancaVirtual(forms.ModelForm):
    class Meta:
        model = BancaVirtual
        fields = ["numeroCuentaDestino", "dniTitularCuentaDestino", "titularCuentaDestino", "transaccion"]

class FormularioCaja(forms.ModelForm):
    class Meta:
        model = Caja
        fields = ["nombres", "apellidos", "transaccion"]

class FormularioCajeroAutomatico(forms.ModelForm):
    class Meta:
        model = CajeroAutomatico
        fields = ["codigo", "ubicacion", "transaccion"]
