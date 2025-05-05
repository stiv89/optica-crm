from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from clientes import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clientes.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)