from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('clientes_con_beneficios/', views.clientes_con_beneficios, name='clientes_con_beneficios'),
    path('registrar_visita/', views.registrar_visita_rapida, name='registrar_visita_rapida'),
    path('clientes/', views.clientes_lista, name='clientes_lista'),
    path('clientes/nuevo/', views.clientes_nuevo, name='clientes_nuevo'),
    path('visitas/', views.visitas_lista, name='visitas_lista'),
    path('visita/<int:visita_id>/', views.detalle_visita, name='detalle_visita'),
    path('clientes/<int:cliente_id>/', views.cliente_detalle, name='cliente_detalle'),
    path('clientes/<int:cliente_id>/editar/', views.cliente_editar, name='cliente_editar'),
    path('clientes/<int:cliente_id>/eliminar/', views.cliente_eliminar, name='cliente_eliminar'),
    path('visitas/', views.visitas_lista, name='visitas_lista'),
    path("crear-superuser/", views.crear_superusuario, name="crear_superuser"),
    path("setup-admin/", views.setup_admin, name="setup_admin"),
    path('login/', views.login_view, name='login'),
]
