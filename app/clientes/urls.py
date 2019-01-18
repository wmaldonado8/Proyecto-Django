from django.urls import path

from . import views

urlpatterns = [
    path('', views.principal, name = 'cliente'),
    path('primerMensaje', views.saludar),
    path('nuevo', views.crear),
    path('buscar', views.buscar),
    path('buscarCuenta', views.buscarCuenta),
    path('editar', views.modificar),
    path('eliminar', views.eliminar),
    path('cuentas', views.principalCuenta),
    path('crearCuenta', views.crearCuenta),
    path('transaccion', views.transaccion),
    path('verTransaccion', views.verTransaccion),
    path('transferencia', views.crearTransferencia),
    path('buscarCuentaTransferencia', views.buscarTrans),

]
